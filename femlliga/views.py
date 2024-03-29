import os
import exif
import json
import time
import uuid
import logging
import datetime
import unicodedata

from io import BytesIO
from pathlib import Path
from functools import cmp_to_key, reduce

from django.http import Http404, JsonResponse
from django.forms import formset_factory, inlineformset_factory
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage, mail_managers
from django.utils import timezone
from django.utils.cache import patch_response_headers
from django.core.exceptions import PermissionDenied
from django.views.static import serve
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.loader import render_to_string

import networkx as nx

from config.settings import MEDIA_ROOT
from .models import *
from .constants import *
from .forms import *
from .utils import clean_form_email, get_next_resource, get_resource_index, get_json_body

def require_own_organization(func):
    def decorated(request, organization_id, *args, **kwargs):
        organization = Organization.objects.get(pk = organization_id)
        if request.user != organization.creator:
            raise PermissionDenied()

        return func(request, organization_id, *args, **kwargs)
    return decorated

def require_own_agreement(func):
    def decorated(request, organization_id, agreement_id, *args, **kwargs):
        organization = Organization.objects.get(pk = organization_id)
        if request.user != organization.creator:
            raise PermissionDenied()

        a = Agreement.objects.get(pk = agreement_id)
        if a.solicitor != organization and a.solicitee != organization:
            raise PermissionDenied()

        return func(request, organization_id, agreement_id, *args, **kwargs)
    return decorated

def record_stats(name):
    def f(func):
        def decorated(request, organization_id, *args, **kwargs):
            start = time.time()
            r = func(request, organization_id, *args, **kwargs)
            logging.warning(f"Handler {name} took {time.time() - start}")
            return r
        return decorated
    return f

def index(request):
    return render(request, "femlliga/index.html", {"form": ContactForm()})

def page(request, name):
    try:
        page = get_object_or_404(Page, name=name)
    except:
        if name in ["faq", "legal", "privacy", "accessibility"]:
            page = Page(name=name, heading="Títol", subheading="Subtítol", content="<p>Cal definir aquesta pàgina</p>")
            page.save()
        else:
            raise
    return render(request, "femlliga/page.html", { "page": page })

def check_matches(request):
    if request.method != "POST":
        return JsonResponse({})

    post = get_json_body(request)
    resource = post.get("resource", "")
    option = post.get("option", "")

    needs = Need.objects.filter(resource=resource, has_resource=True, options__name__in=[option]).count()
    offers = Offer.objects.filter(resource=resource, has_resource=True, options__name__in=[option]).count()
    return JsonResponse({ "needs": needs, "offers": offers })

@login_required
def app(request):
    orgs = organization_prefetches(request.user.organizations.all(), include_missing_resources=True)
    if len(orgs) == 0:
        return redirect("add_organization")

    org = orgs[0]
    if not org.resources_set:
        return redirect("pre-wizard", organization_id=org.id)

    own_needs = sort_resources([
        n for n in org.needs.all().prefetch_related("options") if n.has_resource and n.resource != "OTHER"
    ])
    offer_matches, need_matches = get_organization_matches(org, own_needs)
    return render(request, "femlliga/app.html", {
        "org": org,
        "needs": [n for n in org.needs.all() if n.has_resource],
        "offers": [n for n in org.offers.all() if n.has_resource],
        "offer_matches": offer_matches,
        "need_matches": need_matches,
    })

@login_required
@require_own_organization
def pre_wizard(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if not org.needs_not_set():
        return redirect("mid-wizard", organization_id=org.id)
    return aux_wizard(request, organization_id, "needs", "pre-wizard")

@login_required
@require_own_organization
def mid_wizard(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if not org.offers_not_set():
        return redirect("post-wizard", organization_id=org.id)
    return aux_wizard(request, organization_id, "offers", "mid-wizard")

@login_required
@require_own_organization
def post_wizard(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        org.resources_set = True
        org.save()
        return redirect("matches", organization_id=org.id)
    return render(request, "femlliga/aux-wizard.html", {"org": org, "page": "post-wizard"})

@login_required
@require_own_organization
def reset_wizard(request, organization_id):
    if request.method == "POST":
        org = get_object_or_404(Organization, pk=organization_id)
        org.resources_set = False
        org.save()
        return redirect("pre-wizard", organization_id=org.id)

def aux_wizard(request, organization_id, resource_type, page):
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        if request.POST["start"] == "yes":
            first_not_set = org.first_resource_not_set(resource_type)
            return redirect("resources-wizard", organization_id=org.id, resource_type=resource_type, resource=first_not_set)
        else:
            org.resources_set = True
            org.save()
            return redirect("app")
    return render(request, "femlliga/aux-wizard.html", { "org": org, "page": page })

@login_required
def add_organization(request):
    if request.method == "POST":
        return process_organization_post(request)

    return render(request, "femlliga/add_organization.html", {
        "form": OrganizationForm(),
        "org": None,
        "social_media_forms": social_media_forms()(),
    })

@login_required
def view_organization(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    return render(request, "femlliga/view_organization.html", { "org": org })

@login_required
@require_own_organization
def profile(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    return render(request, "femlliga/profile.html", { "org": org })

@login_required
@require_own_organization
def edit_organization(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        return process_organization_post(request, org = org)

    return render(request, "femlliga/add_organization.html", {
        "edit": True,
        "form": OrganizationForm({
            "name": org.name,
            "description": org.description,
            "org_type": org.org_type,
            "scopes": [x.name for x in org.scopes.all()],
            "lat": org.lat,
            "lng": org.lng,
            "address": org.address,
        }),
        "org": org,
        "social_media_forms": social_media_forms()(instance=org),
    })

@login_required
@require_own_organization
def delete_organization_logo(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        org.logo.delete()
    return JsonResponse({"ok": True})

def social_media_forms():
    return inlineformset_factory(
        Organization,
        SocialMedia,
        fields=("media_type", "value"),
        extra=len(SOCIAL_MEDIA_TYPES),
    )

def process_organization_post(request, org = None):
    form = OrganizationForm(request.POST, request.FILES)
    socialmedia_formset = social_media_forms()(request.POST, instance=org)
    if form.is_valid() and socialmedia_formset.is_valid():
        if org is None:
            org = Organization()
            socialmedia_formset.instance = org
        lat = form.cleaned_data["lat"]
        lng = form.cleaned_data["lng"]
        org.name = form.cleaned_data["name"]
        org.description = form.cleaned_data["description"]
        org.org_type = form.cleaned_data["org_type"]
        org.address = form.cleaned_data.get("address", None)
        org.lat = lat
        org.lng = lng
        org.city = get_city_from_coordinates(lat, lng)
        org.creator = request.user
        if form.cleaned_data["logo"]:
            file = clean_file(form.cleaned_data["logo"])
            org.logo = file
        org.save()
        socialmedia_formset.save()
        for scope in ORG_SCOPES:
            s = OrganizationScope(name = scope[0])
            s.save()
            if scope[0] in form.cleaned_data["scopes"]:
                org.scopes.add(s)
            else:
                org.scopes.remove(s)

        return redirect("app")

    return render(request, "femlliga/add_organization.html", {
        "form": form,
        "org": org,
        "social_media_forms": socialmedia_formset,
        "edit": org != None,
    })

@login_required
@require_own_organization
def edit_resources_wizard(request, organization_id, resource_type, resource):
    assert_url_param_in_list(resource_type, ["needs", "offers"])
    assert_url_param_in_list(resource, RESOURCES_LIST)
    if request.method == "POST":
        return resources_wizard(request, organization_id, resource_type, resource, editing = True)

    org = get_object_or_404(Organization, pk=organization_id)
    model, imagemodel = get_resources_models(resource_type)
    try:
        r = model.objects.get(organization = org, resource = resource)
        data = {
            "resource": resource,
            "options": list(map(lambda x: x.name, r.options.all())),
            "has_resource": r.has_resource,
            "comments": r.comments,
        }
        try:
            data["charge"] = r.charge
        except:
            pass # field only exists for offers
        form = ResourceForm(data)
    except:
        r = None
        form = ResourceForm()

    return render_wizard(request, org, resource, form, resource_type, editing = True, db_resource = r)

def get_resources_models(resource_type):
    if resource_type == "offers":
        return Offer, OfferImage
    return Need, NeedImage

def render_wizard(request, org, resource, form, resource_type, editing = False, db_resource = None, imageforms=None):
    model, imagemodel = get_resources_models(resource_type)
    if not imageforms:
        imageforms = inlineformset_factory(model, imagemodel, fields=("image",), extra=6)()
    return render(request, "femlliga/resources-wizard.html", {
        "org": org,
        "resource": Resource.resource(resource),
        "db_resource": db_resource,
        "form": form,
        "resource_type": resource_type,
        "imageforms": imageforms,
        "total": len(RESOURCES) * 2,
        "count": get_resource_index(resource_type, resource),
        "editing": editing,
    })

@login_required
@require_own_organization
def resources_wizard(request, organization_id, resource_type, resource, editing = False):
    assert_url_param_in_list(resource_type, ["needs", "offers"])
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        model, imagemodel = get_resources_models(resource_type)
        try:
            m = model.objects.get(resource = resource, organization = org)
        except Exception as ex:
            m = model(resource = resource, organization = org)
            m.save()

        ImageFormSet = inlineformset_factory(model, imagemodel, fields=("image",))
        imageformset = ImageFormSet(request.POST, clean_files(request.FILES), instance = m)

        form = ResourceForm(request.POST)
        if resource_type == "needs":
            forms_valid = form.is_valid()
        else:
            forms_valid = form.is_valid() and imageformset.is_valid()
        if forms_valid:
            for option, _ in Resource.resource(resource).options():
                ro = ResourceOption(name=option)
                ro.save()
                if option in form.cleaned_data["options"]:
                    m.options.add(ro)
                else:
                    m.options.remove(ro)

            m.comments = form.cleaned_data["comments"]
            m.has_resource = form.cleaned_data["has_resource"] == "yes"
            m.charge = form.cleaned_data["charge"]
            m.save()
            if resource_type == "offers":
                imageformset.save()
                for name in request.POST:
                    if name.startswith("delete-image-"):
                        name = name.removeprefix("delete-image-")
                        try:
                            image_id = int(name)
                            image = imagemodel.objects.get(pk = image_id)
                            if image.resource.organization != org:
                                continue
                            f = Path(image.image.path)
                            if f.is_file():
                                f.unlink()
                            image.delete()
                        except Exception as ex:
                            raise

            return redirect_resource_set(org, resource_type, resource)
        else:
            return render_wizard(request, org, resource, form, resource_type, editing = editing, db_resource=m, imageforms=imageformset)

    return render_wizard(request, org, resource, ResourceForm(), resource_type)

def redirect_resource_set(org, resource_type, resource):
    if org.resources_set:
        return redirect("app")

    next_resource = get_next_resource(resource)
    if next_resource is None:
        if resource_type == "needs":
            return redirect("mid-wizard", organization_id=org.id)
        else:
            return redirect("post-wizard", organization_id=org.id)

    return redirect("resources-wizard", organization_id=org.id, resource_type=resource_type, resource=next_resource)

def clean_files(FILES):
    for key in FILES:
        FILES[key] = clean_file(FILES[key])

    return FILES

def clean_file(posted_file):
    filename = str(uuid.uuid4()) + Path(posted_file.name).suffix
    try:
        f = exif.Image(posted_file.read())
        f.delete_all()
        f = f.get_file()
        posted_file = InMemoryUploadedFile(
            BytesIO(f),
            posted_file.field_name,
            filename,
            posted_file.content_type,
            len(f),
            posted_file.charset,
        )
        return posted_file
    except:
        posted_file.seek(0)
        posted_file.name = filename
        return posted_file # exif will not work for files other than JPEG

@login_required
@require_own_organization
@record_stats("matches")
def matches(request, organization_id):
    # TODO better matches computation, does much more work than needed
    organization = request.user.organizations.first()
    own_needs = sort_resources([
        n for n in organization.needs.all().prefetch_related("options") if n.has_resource and n.resource != "OTHER"
    ])
    needs_json = [{
        "resource": x.resource,
        "options": [o.name for o in x.options.all()],
    } for x in own_needs]
    agreement_declined_map = get_last_agreement_declined_map(organization)
    offer_matches, need_matches = get_organization_matches(organization, own_needs)
    organization_matches = group_matches_by_organization(organization, offer_matches, need_matches)
    matches = {}
    for need in needs_json:
        need = need["resource"]
        matches[need] = [
            m.json(current_organization=organization, agreement_declined_map=agreement_declined_map)
            for l in organization_matches
            for m in filter(lambda x: x.resource == need, l)
        ]
    return render_matches_page(request, "femlliga/matches.html", organization, matches, needs_json)

def render_matches_page(request, template, organization, matches, needs_json, organization_matches=None):
    json_data = {
        "matches": matches,
        "needs": needs_json,
        "resource_names_map": RESOURCE_NAMES_MAP,
        "option_names_map": RESOURCE_OPTIONS_DEF_MAP,
        "resource_icons_map": RESOURCE_ICONS_MAP,
    }
    if organization_matches:
        json_data["organization_matches"] = organization_matches
    return render(request, template, { "json_data": json_data })

def get_last_agreement_declined_map(organization):
    l = list(Agreement.objects.prefetch_related("solicitee").filter(solicitor=organization).exclude(communication_accepted=None))
    return {
        "need": get_last_agreement_declined_map_resource(list(filter(lambda x: x.resource_type=="need", l))),
        "offer": get_last_agreement_declined_map_resource(list(filter(lambda x: x.resource_type=="offer", l))),
    }

def get_last_agreement_declined_map_resource(l):
    return {
        k[0]: get_last_agreement_declined_map_organization(list(filter(lambda x: x.resource==k[0], l))) for k in RESOURCES
    }

def get_last_agreement_declined_map_organization(l):
    org_ids = set([x.solicitee.id for x in l])
    return {
        id: get_last_agreement_declined(list(filter(lambda x: x.solicitee.id==id, l))) for id in org_ids
    }

def get_last_agreement_declined(l):
    ll = list(sorted(l, key=lambda x: x.communication_date, reverse=True))
    if len(ll) > 0:
        return not ll[0].communication_accepted
    return False

def group_matches_by_organization(organization, offer_matches, need_matches):
    orgs = {}
    for k in offer_matches:
        for m in offer_matches[k]:
            try:
                orgs[m.organization.id].append(m)
            except:
                orgs[m.organization.id] = [m]
    for k in need_matches:
        for m in need_matches[k]:
            try:
                orgs[m.organization.id].append(m)
            except:
                orgs[m.organization.id] = [m]

    return [orgs[k] for k in sorted(orgs.keys(), key=lambda k: orgs[k][0].organization.distance(organization))]

def get_organization_matches(organization, own_needs):
    offer_matches, need_matches = {}, {}
    for need in own_needs:
        need_options = [n.name for n in need.options.all()]
        offers = get_model_matches(organization, need.resource, Offer, need_options = need_options, include_other=False)
        if len(offers) > 0:
            offer_matches[need.resource] = offers

        needs = get_model_matches(organization, need.resource, Need, need_options = need_options, include_other=False)
        if len(needs) > 0:
            need_matches[need.resource] = needs

    return offer_matches, need_matches

def get_model_matches(organization, resource, model, need_options = None, include_other=True):
    if need_options is None:
        queryset = model.objects.filter(
            resource = resource,
            has_resource = True,
        )
    else:
        queryset = model.objects.filter(
            resource = resource,
            has_resource = True,
            options__name__in = need_options,
        )

    if not include_other:
        queryset = queryset.exclude(resource="OTHER")

    results = queryset.\
    exclude(organization=organization).\
    prefetch_related("organization").\
    prefetch_related("images").\
    prefetch_related("options").\
    distinct()
    return sorted(results, key=lambda r: r.organization.distance(organization))

def get_all_resources(organization):
    offer_matches, need_matches = {}, {}
    for resource in RESOURCES:
        offers = get_model_matches(organization, resource[0], Offer)
        if len(offers) > 0:
            offer_matches[resource[0]] = offers

        needs = get_model_matches(organization, resource[0], Need)
        if len(needs) > 0:
            need_matches[resource[0]] = needs

    return offer_matches, need_matches

@login_required
@require_own_organization
@record_stats("search")
def search(request, organization_id):
    organization = organization_prefetches(request.user.organizations.filter(id=organization_id)).first()
    offer_matches, need_matches = get_all_resources(organization)
    organization_matches = group_matches_by_organization(organization, offer_matches, need_matches)
    agreement_declined_map = get_last_agreement_declined_map(organization)
    matches = {
        "offerMatches": {
            k: [m.json(
                current_organization=organization,
                agreement_declined_map=agreement_declined_map,
            ) for m in offer_matches[k]] for k in offer_matches
        },
        "needMatches": {
            k: [m.json(
                current_organization=organization,
                agreement_declined_map=agreement_declined_map,
            ) for m in need_matches[k]] for k in need_matches
        },
    }
    organization_matches = [
        {
            "organization": l[0].organization.json(current_organization=organization),
            "matches": [m.json(
                current_organization=organization,
                agreement_declined_map=agreement_declined_map,
            ) for m in l],
        }
        for l in organization_matches
    ]
    return render_matches_page(request, "femlliga/search.html", organization, matches, [x[0] for x in RESOURCES], organization_matches = organization_matches)

@login_required
def preferences(request):
    form = PreferencesForm({
        "notifications_frequency": request.user.notifications_frequency,
        "accept_communications_automatically": request.user.accept_communications_automatically,
    })
    if request.method == "POST":
        form = PreferencesForm(request.POST)
        if form.is_valid():
            request.user.notifications_frequency = form.cleaned_data["notifications_frequency"]
            request.user.accept_communications_automatically = form.cleaned_data["accept_communications_automatically"]
            request.user.save()
            messages.info(request, "La configuració s'ha desat correctament", extra_tags="show")
            return redirect("preferences")

    return render(request, "femlliga/preferences.html", {
        "form": form,
    })

@login_required
@require_own_organization
def send_message(request, organization_id, organization_to, resource_type, resource):
    if request.method != "POST":
        return JsonResponse({})

    assert_url_param_in_list(resource_type, ["need", "offer"])
    assert_url_param_in_list(resource, RESOURCES_LIST)
    organization = get_object_or_404(Organization, pk = organization_id)
    other = get_object_or_404(Organization, pk = organization_to)
    model = Offer
    if resource_type == "need":
        model = Need
    r = get_object_or_404(model, organization=other, resource = resource)
    post = get_json_body(request)
    form = MessageForm(post, resource=r)
    if form.is_valid():
        a = Agreement(
            solicitor=organization,
            solicitee=other,
            message=form.cleaned_data["message"],
            resource=resource,
            resource_type=resource_type,
        )
        a.save()
        for option in form.cleaned_data["options"]:
            ro = ResourceOption(name=option)
            ro.save()
            a.options.add(ro)

        if other.creator.accept_communications_automatically:
            do_agreement_connect(request, a, True)

        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False})

@login_required
@require_own_organization
def agreements(request, organization_id):
    organization = get_object_or_404(Organization, pk = organization_id)
    sent = sort_agreements(organization.sent_agreements.all())
    received = sort_agreements(organization.received_agreements.all())
    agreements_by_organization = group_agreements_by_organizations(sort_agreements(sent + received), organization)
    organization_names_map_json = {}
    for agreements in agreements_by_organization:
        org = agreement_other_organization(agreements[0], organization_id)
        organization_names_map_json[str(org.id)] = org.name
    return render(request, f"femlliga/agreements.html", {
        "org": organization,
        "agreements": { "sent": sent, "received": received },
        "agreements_json": {
            "sent": group_agreements_by_resource_json(sent, organization_id),
            "received": group_agreements_by_resource_json(received, organization_id),
        },
        "concatenated_agreements_json": [a.json(organization_id) for a in sort_agreements(sent+received)],
        "organizations_json": [
            {
                "organization": agreement_other_organization(l[0], organization_id).json(current_organization=organization),
                "agreements": [a.json(organization_id) for a in l]
            }
            for l in agreements_by_organization
        ],
        "organization_names_map_json": organization_names_map_json,
        "requested_resources_json": { "sent": requested_resources(sent), "received": requested_resources(received) },
    })

def requested_resources(agreements):
    return sorted(set([a.resource for a in agreements]))

def group_agreements_by_resource_json(l, organization_id):
    m = {}
    for x in l:
        try:
            m[x.resource].append(x.json(organization_id))
        except:
            m[x.resource] = [x.json(organization_id)]
    return m

def group_agreements_by_organizations(agreements, organization):
    orgs = {}
    for a in agreements:
        try:
            orgs[agreement_other_organization(a, organization.id).id].append(a)
        except:
            orgs[agreement_other_organization(a, organization.id).id] = [a]

    return [orgs[k] for k in sorted(orgs.keys(), key=lambda k: agreement_other_organization(orgs[k][0], organization.id).distance(organization))]

def agreement_other_organization(agreement, organization_id):
    if agreement.solicitor.id == organization_id:
        return agreement.solicitee
    return agreement.solicitor

@login_required
@require_own_agreement
def agreement_successful(request, organization_id, agreement_id):
    if request.method != "POST":
        return JsonResponse({})

    a = get_object_or_404(Agreement, pk = agreement_id)
    post = get_json_body(request)
    a.agreement_successful = post["successful"] == "yes"
    a.successful_date = timezone.now()
    a.save()

    return JsonResponse({"ok": True})

@login_required
@require_own_agreement
def agreement_connect(request, organization_id, agreement_id):
    if request.method != "POST":
        return JsonResponse({})

    a = get_object_or_404(Agreement, pk = agreement_id)
    organization = get_object_or_404(Organization, pk = organization_id)
    post = get_json_body(request)
    if organization != a.solicitee:
        return # user owns organization; only solicitee organization should be able to accept

    do_agreement_connect(request, a, post["connect"] == "yes")

    return JsonResponse({"ok": True})

def do_agreement_connect(request, a, communication_accepted):
    a.communication_accepted = communication_accepted
    a.communication_date = timezone.now()
    a.save()
    if a.communication_accepted:
        subject = f"Comunicació iniciada per compartir {resource_name(a.resource)}"
        body = render_to_string("email/agreement_connect.html", {
            "a": a,
            "current_site": get_current_site(request),
        })
        to_list = [a.solicitor.creator.email, a.solicitee.creator.email]
        msg = EmailMessage(subject=subject, body=body, from_email=FROM_EMAIL, to=to_list)
        msg.content_subtype = "html"
        msg.send()

def get_city_from_coordinates(lat, lng):
    """Nominatim also accepts a search option that gives coordinates given a place's name"""
    try:
        res = http_get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}")
        try:
            return res["address"]["city"]
        except:
            return res["address"]["town"]
    except:
        return "Unknown city"

def organization_prefetches(queryset, include_missing_resources=False):
    if include_missing_resources:
        queryset = queryset.prefetch_related("needs").prefetch_related("offers")
    else:
        queryset = queryset.\
            prefetch_related(Prefetch("needs", queryset=Need.objects.filter(has_resource=True))).\
            prefetch_related(Prefetch("offers", queryset=Offer.objects.filter(has_resource=True)))
    return queryset.\
        prefetch_related("scopes").\
        prefetch_related("social_media").\
        prefetch_related("needs__options").\
        prefetch_related("offers__options").\
        prefetch_related("needs__images").\
        prefetch_related("offers__images").\
        prefetch_related("sent_agreements__options").\
        prefetch_related("received_agreements__options")

@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    return render(request, "femlliga/dashboard.html", {
        "organizations": Organization.objects.count(),
        "agreements": Agreement.objects.count(),
        "contacts": Contact.objects.count(),
    })

@user_passes_test(lambda u: u.is_staff)
def report(request):
    organizations = organization_prefetches(Organization.objects.all())

    orgs_json = list(map(lambda o: {"name": o.name, "lat": float(o.lat), "lng": float(o.lng)}, organizations))

    def offers_needs_orgs(orgs):
        return [
            count(orgs, lambda x: x.offers.all()),
            count(orgs, lambda x: x.needs.all()),
            len(orgs),
        ]

    def offers_charge_orgs(orgs):
        return [
            count(orgs, lambda x: [r for r in x.offers.all() if r.charge]),
            count(orgs, lambda x: [r for r in x.offers.all() if not r.charge]),
        ]

    def agreements_orgs(orgs, f):
        return [
            count(orgs, lambda x: [a for a in f(x) if a.communication_accepted==None]),
            count(orgs, lambda x: [a for a in f(x) if a.communication_accepted==True and a.agreement_successful==None]),
            count(orgs, lambda x: [a for a in f(x) if a.communication_accepted==False]),
            count(orgs, lambda x: [a for a in f(x) if a.communication_accepted==True and a.agreement_successful==True]),
            count(orgs, lambda x: [a for a in f(x) if a.communication_accepted==True and a.agreement_successful==False]),
            count(orgs, lambda x: [a for a in f(x)]),
        ]

    org_types, resources_by_org_type, agreements_by_solicitor_type, agreements_by_solicitee_type  = [], [], [], []
    charge_by_org_type = []
    for org_type in sort_by_name(ORG_TYPES):
        orgs = [o for o in organizations if o.org_type == org_type[0]]
        org_types.append(org_type_name(org_type[0]))
        resources_by_org_type.append(offers_needs_orgs(orgs))
        charge_by_org_type.append(offers_charge_orgs(orgs))
        agreements_by_solicitor_type.append(agreements_orgs(orgs, lambda x: x.sent_agreements.all()))
        agreements_by_solicitee_type.append(agreements_orgs(orgs, lambda x: x.received_agreements.all()))

    org_scopes, resources_by_org_scope, agreements_by_solicitor_scope, agreements_by_solicitee_scope = [], [], [], []
    for scope in sort_by_name(ORG_SCOPES):
        orgs = [o for o in organizations if o.has_scope(scope[0])]
        org_scopes.append(org_scope_name(scope[0]))
        resources_by_org_scope.append(offers_needs_orgs(orgs))
        agreements_by_solicitor_scope.append(agreements_orgs(orgs, lambda x: x.sent_agreements.all()))
        agreements_by_solicitee_scope.append(agreements_orgs(orgs, lambda x: x.received_agreements.all()))

    resource_names, resources_by_resource_type, agreements_by_resource_type = [], [], []
    charge_by_resource_type = []
    for resource in RESOURCES_ORDER:
        needs, offers = [], []
        for o in organizations:
            for x in o.needs.all():
                if x.resource==resource:
                    needs.append(x)
            for x in o.offers.all():
                if x.resource==resource:
                    offers.append(x)
        resource_names.append(resource_name(resource))
        resources_by_resource_type.append([len(offers), len(needs)])
        charge_by_resource_type.append([len([x for x in offers if x.charge]), len([x for x in offers if not x.charge])])
        agreements_by_resource_type.append(agreements_orgs(
            organizations, lambda x: [a for a in x.sent_agreements.all() if a.resource==resource]))

    resource_options, resources_by_resource_option = [], []
    for resource in RESOURCES_ORDER:
        for option in RESOURCE_OPTIONS_MAP[resource]:
            needs, offers = [], []
            for o in organizations:
                for x in o.needs.all():
                    if x.resource == resource and option[0] in [op.name for op in x.options.all()]:
                        needs.append(x)
                for x in o.offers.all():
                    if x.resource == resource and option[0] in [op.name for op in x.options.all()]:
                        offers.append(x)
            resource_options.append("{} - {}".format(resource_name(resource), option_name(option[0])))
            resources_by_resource_option.append([len(offers), len(needs)])

    agreements_header = ["Pendents de comunicació", "Comunicació iniciada", "Comunicació rebutjada", "Acord aconseguit", "Acord no aconseguit", "Total"]
    agreements_started = list(map(lambda o: o.date, Agreement.objects.all()))
    agreements_comm = list(map(lambda o: o.communication_date, Agreement.objects.filter(communication_accepted=True)))
    agreements_success = list(map(lambda o: o.successful_date, Agreement.objects.filter(agreement_successful=True)))

    graph = get_relationships_graph()
    other_needs = Need.objects.filter(resource="OTHER").exclude(comments="").exclude(comments=None)
    other_offers = Offer.objects.filter(resource="OTHER").exclude(comments="").exclude(comments=None)
    most_needed = count_word_freqs(" ".join(map(lambda x: x.comments, other_needs)))
    most_offered = count_word_freqs(" ".join(map(lambda x: x.comments, other_offers)))
    return render(request, "femlliga/report.html", {
        "orgs_json": json.dumps(orgs_json),
        "organizations": Timeline(list(map(lambda o: o.date, organizations)), name="Altes d'entitats"),

        "resources_by_org_type": Table(
            ["Recursos per tipus d'entitat", "Oferiments", "Necessitats", "Entitats"], org_types,
            resources_by_org_type),
        "charge_by_org_type": Table(
            ["Oferiments que es cobren per tipus d'entitat", "Oferiments cobrant", "Oferiments gratuïts"], org_types,
            charge_by_org_type),
        "resources_by_org_scope": Table(
            ["Recursos per àmbit de treball de l'entitat", "Oferiments", "Necessitats", "Entitats"], org_scopes,
            resources_by_org_scope),
        "resources_by_resource_type": Table(
            ["Recursos per tipus de recurs", "Oferiments", "Necessitats"], resource_names,
            resources_by_resource_type),
        "charge_by_resource_type": Table(
            ["Oferiments que es cobren per tipus de recurs", "Oferiments cobrant", "Oferiments gratuïts"],
            resource_names, charge_by_resource_type),
        "resources_by_resource_option": Table(
            ["Recursos per tipus concret de recurs", "Oferiments", "Necessitats"], resource_options,
            resources_by_resource_option),

        "agreements_by_solicitor_type": Table(
            ["Interaccions per tipus d'entitat sol·licitant"] + agreements_header, org_types,
            agreements_by_solicitor_type),
        "agreements_by_solicitor_scope": Table(
            ["Interaccions per àmbit de treball de l'entitat sol·licitant"] + agreements_header, org_scopes,
            agreements_by_solicitor_scope),

        "agreements_by_solicitee_type": Table(
            ["Interaccions per tipus d'entitat sol·licitada"] + agreements_header, org_types,
            agreements_by_solicitee_type),
        "agreements_by_solicitee_scope": Table(
            ["Interaccions per àmbit de treball de l'entitat sol·licitada"] + agreements_header, org_scopes,
            agreements_by_solicitee_scope),

        "agreements_by_resource_type": Table(
            ["Interaccions per tipus de recurs"] + agreements_header, resource_names,
            agreements_by_resource_type),

        "agreements_started": Timeline(agreements_started, name="Peticions de col·laboració"),
        "agreements_comm": Timeline(agreements_comm, name="Comunicació acceptada"),
        "agreements_success": Timeline(agreements_success, name="Col·laboració exitosa"),

        "graph": graph,
        "other_needs": other_needs,
        "other_offers": other_offers,
        "most_needed": most_needed,
        "most_offered": most_offered,
        "needs_comments": Need.objects.exclude(resource="OTHER").exclude(comments=""),
        "offers_comments": Offer.objects.exclude(resource="OTHER").exclude(comments=""),
    })

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def count_word_freqs(s):
    l, freqs = strip_accents(s.lower()).split(), {}
    for x in l:
        if x not in freqs:
            freqs[x] = 1
        else:
            freqs[x] += 1

    l = []
    for x in freqs:
        l.append((x, freqs[x]))

    return sorted(l, key=lambda x: x[1], reverse=True)

def get_relationships_graph():
    orgs = Organization.objects.all()
    agreements = Agreement.objects.all().prefetch_related("solicitor").prefetch_related("solicitee")
    relations = {}
    for agreement in agreements:
        key = (agreement.solicitor.id, agreement.solicitee.id)
        if key not in relations.keys():
            relations[key] = 1
        else:
            relations[key] += 1

    edges = []
    for key in relations:
        edges.append((key[0], key[1], relations[key]))

    DG = nx.DiGraph()
    DG.add_weighted_edges_from(edges)
    return Graph(DG)

def sort_by_name(l):
    return sorted(l, key = lambda x: x[1])

def count(orgs, f):
    return reduce(lambda a, b: a+len(f(b)), orgs, 0)

def contact(request):
    if request.method != "POST":
        return render(request, "femlliga/contact.html", { "form": ContactForm() })

    form = ContactForm(request.POST)
    form_sent = False
    if form.is_valid():
        email = form.cleaned_data["email"]
        content = form.cleaned_data["content"]
        if ContactDenyList.objects.filter(email=clean_form_email(email)).count() > 0:
            logging.warning(f"Ignoring SPAM message from {email}")
            return render(request, "femlliga/contact.html", {"form": ContactForm(), "form_sent": True})

        Contact(
            email = email,
            content = content,
        ).save()
        # send contact to managers
        mail_managers(
            f"S'ha rebut un contacte a la web de {APP_NAME}",
            f"Des del correu {email} envien el següent missatge:\n\n{content}",
        )

        # send confirmation to user
        body = render_to_string("email/contact_received.html", {
            "content": content,
            "current_site": get_current_site(request),
        })
        msg = EmailMessage(
            subject=f"El formulari de contacte amb {APP_NAME} s'ha enviat correctament",
            body=body,
            from_email=FROM_EMAIL,
            to=[email],
        )
        msg.content_subtype = "html"
        msg.send()
        form_sent = True
    return render(request, "femlliga/contact.html", {"form": form, "form_sent": form_sent})

@login_required
def uploads(request, path):
    return serve(request, path, MEDIA_ROOT)

def assert_url_param_in_list(param, l):
    if param not in l:
        raise Http404("Unknown parameter")

def most_requested(resources):
    m = {}
    for r in resources:
        if r.resource in m.keys():
            m[r.resource] += 1
        else:
            m[r.resource] = 1
    l = []
    for k in m:
        l.append((m[k], k))
    return sorted(l, reverse=True)

def sort_agreements(agreements):
    def f(a, b):
        if a.communication_accepted is None:  return -1
        if b.communication_accepted is None:  return  1
        if a.communication_accepted is False: return  1
        if b.communication_accepted is False: return -1
        if a.agreement_successful is None:    return -1
        if b.agreement_successful is None:    return  1
        if a.agreement_successful is True:    return -1
        if b.agreement_successful is True:    return  1
        return a.date < b.date

    return sorted(agreements, key=cmp_to_key(f))
