import json
import logging
import time
import unicodedata
import urllib
import uuid
import collections
import pandas as pd

from io import BytesIO
from pathlib import Path
from asgiref.sync import async_to_sync

import exif
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import mail_managers
from django.db.models import Prefetch
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language_from_request
from django.utils.translation import gettext_lazy as _
from django.views.static import serve

from config.settings import MEDIA_ROOT, STAGING_ENVIRONMENT_NAME

from .constants import (
    ORG_SCOPES,
    ORG_TYPES,
    RESOURCE_ICONS_MAP,
    RESOURCE_NAMES_MAP,
    RESOURCE_OPTIONS_QUESTION_MAP,
    RESOURCE_OPTIONS_DEF_MAP,
    RESOURCE_OPTIONS_MAP,
    RESOURCE_OPTIONS_WITH_PREFIX,
    RESOURCES,
    RESOURCES_LIST,
    RESOURCES_ORDER,
    SOCIAL_MEDIA_TYPES,
    NEEDS_PUBLISHABLE_OPTIONS_LABELS_MAP_2,
    NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP_2,
)

from .forms import (
    ContactForm,
    MessageForm,
    OrganizationForm,
    PreferencesForm,
    ResourceForm,
    AnnouncementForm,
    AnnouncementContactForm,
    ReportFilterForm,
)

from .models import (
    Agreement,
    Announcement,
    AnnouncementContact,
    Contact,
    ContactDenyList,
    Message,
    Need,
    NeedImage,
    Offer,
    OfferImage,
    Organization,
    OrganizationScope,
    Page,
    Resource,
    ResourceOption,
    SocialMedia,
    ExcludeCommentWord,
    option_name,
    org_scope_name,
    org_type_name,
    resource_name,
    get_report_statistics,
)

from .utils import (
    strip_accents,
    clean_form_email,
    get_json_body,
    get_next_resource,
    get_own_needs,
    get_resource_index,
    http_get,
    limit_organizations_distance,
    send_email,
    send_notification,
    str_to_bool,
    create_agreement_message,
    date_to_datetime,
)

from .maps import (
    get_femlliga_organizations,
    get_tornallom_organizations,
)

from femlliga.gis.es import spain_provinces


def require_own_organization(func):
    def decorated(request, organization_id, *args, **kwargs):
        organization = get_object_or_404(Organization, pk=organization_id)
        if request.user != organization.creator:
            raise PermissionDenied()

        return func(request, organization_id, *args, **kwargs)

    return decorated


def require_own_agreement(func):
    def decorated(request, organization_id, agreement_id, *args, **kwargs):
        organization = get_object_or_404(Organization, pk=organization_id)
        if request.user != organization.creator:
            raise PermissionDenied()

        a = get_object_or_404(Agreement, pk=agreement_id)
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
    return render(
        request,
        "femlliga/index.html",
        {
            "form": ContactForm(),
            "json_data": {
                "resource_names_map": RESOURCE_NAMES_MAP,
                "resource_options_map": RESOURCE_OPTIONS_MAP,
                "resource_options_question_map": RESOURCE_OPTIONS_QUESTION_MAP,
                "option_names_map": RESOURCE_OPTIONS_DEF_MAP,
            },
        },
    )


def page(request, name):
    lang = get_language_from_request(request)
    try:
        page = get_object_or_404(Page, name=name, language=lang)
    except:
        if name in ["faq", "legal", "privacy", "accessibility"]:
            page = Page.objects.create(
                name=name,
                language=lang,
                heading=_("Títol"),
                subheading=_("Subtítol"),
                content=_("<p>Cal definir aquesta pàgina</p>"),
            )
        else:
            raise
    return render(request, "femlliga/page.html", {"page": page})


def check_matches(request):
    if request.method != "POST":
        return JsonResponse({})

    post = get_json_body(request)
    resource = post.get("resource", "")
    option = post.get("option", "")

    needs = Need.objects.filter(
        resource=resource, has_resource=True, options__name__in=[option]
    ).count()
    offers = Offer.objects.filter(
        resource=resource, has_resource=True, options__name__in=[option]
    ).count()
    return JsonResponse({"needs": needs, "offers": offers})


@login_required
def app(request):
    orgs = organization_prefetches(
        request.user.organizations.all(), include_missing_resources=True
    )
    if len(orgs) == 0:
        return redirect("add_organization")

    org = orgs[0]
    if not org.resources_set:
        return redirect("pre-wizard", organization_id=org.id)

    return render(
        request,
        "femlliga/app.html",
        {
            "org": org,
            "needs": [n for n in org.needs.all() if n.has_resource],
            "offers": [n for n in org.offers.all() if n.has_resource],
        },
    )


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
        return redirect_wizard_finish(org)
    return aux_wizard(request, organization_id, "offers", "mid-wizard")


def redirect_wizard_finish(org):
    org.resources_set = True
    org.save()
    return redirect(
        reverse("matches", kwargs={"organization_id": org.id}) + "?wizard_finished=true"
    )


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
            return redirect(
                "resources-wizard",
                organization_id=org.id,
                resource_type=resource_type,
                resource=first_not_set,
            )
        else:
            org.resources_set = True
            org.save()
            return redirect("app")

    return render(request, "femlliga/aux-wizard.html", {"org": org, "page": page})


@login_required
def add_organization(request):
    if request.method == "POST":
        return process_organization_post(request)

    return render(
        request,
        "femlliga/add_organization.html",
        {
            "form": OrganizationForm(),
            "org": None,
            "social_media_forms": social_media_forms()(),
        },
    )


@login_required
def search_address(request):
    address = urllib.parse.quote(request.GET.get("address", ""))
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    return JsonResponse({"addresses": http_get(url)})


def view_organization(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if not request.user.is_authenticated:
        if org.announcements.filter(public=True).count() == 0:
            raise PermissionDenied()
    return render(request, "femlliga/view_organization.html", {"org": org})


@login_required
@require_own_organization
def profile(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    return render(request, "femlliga/profile.html", {"org": org})


@login_required
@require_own_organization
def edit_organization(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        return process_organization_post(request, existing_org=org)

    return render(
        request,
        "femlliga/add_organization.html",
        {
            "edit": True,
            "form": OrganizationForm(
                {
                    "name": org.name,
                    "description": org.description,
                    "org_type": org.org_type,
                    "scopes": [x.name for x in org.scopes.all()],
                    "lat": org.lat,
                    "lng": org.lng,
                    "address": org.address,
                }
            ),
            "org": org,
            "social_media_forms": social_media_forms()(instance=org),
        },
    )


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


def process_organization_post(request, existing_org=None):
    form = OrganizationForm(request.POST, request.FILES)
    org = existing_org
    socialmedia_formset = social_media_forms()(request.POST, instance=org)
    if form.is_valid() and socialmedia_formset.is_valid():
        if org is None:
            org = Organization(welcome_email_sent=False)
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
            s = OrganizationScope(name=scope[0])
            s.save()
            if scope[0] in form.cleaned_data["scopes"]:
                org.scopes.add(s)
            else:
                org.scopes.remove(s)

        if existing_org:
            return redirect("profile", organization_id=existing_org.id)
        return redirect("app")

    return render(
        request,
        "femlliga/add_organization.html",
        {
            "form": form,
            "org": org,
            "social_media_forms": socialmedia_formset,
            "edit": org is not None,
        },
    )


@login_required
@require_own_organization
def edit_resources_wizard(request, organization_id, resource_type, resource):
    assert_url_param_in_list(resource_type, ["needs", "offers"])
    assert_url_param_in_list(resource, RESOURCES_LIST)
    if request.method == "POST":
        return resources_wizard(
            request, organization_id, resource_type, resource, editing=True
        )

    org = get_object_or_404(Organization, pk=organization_id)
    r, form = get_resource_form(org, resource_type, resource)
    return render_wizard(
        request, org, resource, form, resource_type, editing=True, db_resource=r
    )


def get_resource_form(org, resource_type, resource):
    model, _ = get_resources_models(resource_type)
    try:
        r = model.objects.get(organization=org, resource=resource)
        data = {
            "resource": resource,
            "options": list(map(lambda x: x.name, r.options.all())),
            "has_resource": r.has_resource,
            "comments": r.comments,
        }
        try:
            data["charge"] = r.charge
            data["place_accessible"] = r.place_accessible
        except:
            pass  # field only exists for offers
        form = ResourceForm(data)
    except:
        r = None
        form = ResourceForm()
    return r, form


def get_resources_models(resource_type):
    if resource_type == "offers":
        return Offer, OfferImage
    return Need, NeedImage


def render_wizard(
    request,
    org,
    resource,
    form,
    resource_type,
    editing=False,
    db_resource=None,
    imageforms=None,
):
    model, imagemodel = get_resources_models(resource_type)
    if not imageforms:
        imageforms = inlineformset_factory(
            model, imagemodel, fields=("image",), extra=6
        )()

    selected_options = []
    try:
        selected_options = form.cleaned_data["options"]
    except:
        if db_resource:
            selected_options = [o.name for o in db_resource.options.all()]

    return render(
        request,
        "femlliga/resources-wizard.html",
        {
            "org": org,
            "resource": Resource.resource(resource),
            "db_resource": db_resource,
            "form": form,
            "resource_type": resource_type,
            "imageforms": imageforms,
            "total": len(RESOURCES) * 2,
            "count": get_resource_index(resource_type, resource),
            "editing": editing,
            "json_data": {
                "selected": selected_options,
            },
        },
    )


@login_required
@require_own_organization
def resources_wizard(request, organization_id, resource_type, resource, editing=False):
    assert_url_param_in_list(resource_type, ["needs", "offers"])
    org = get_object_or_404(Organization, pk=organization_id)
    if request.method == "POST":
        model, imagemodel = get_resources_models(resource_type)
        m, _created = model.objects.get_or_create(resource=resource, organization=org)

        ImageFormSet = inlineformset_factory(model, imagemodel, fields=("image",))
        imageformset = ImageFormSet(
            request.POST, clean_files(request.FILES), instance=m
        )

        form = ResourceForm(request.POST)
        if resource_type == "needs":
            forms_valid = form.is_valid()
        else:
            forms_valid = form.is_valid() and imageformset.is_valid()
        if forms_valid:
            options = form.cleaned_data["options"]
            resource_options = []
            for option, _ignore in Resource.resource(resource).options():
                ro, _ignore = ResourceOption.objects.get_or_create(name=option)
                if option in options:
                    resource_options.append(ro)

            m.options.set(resource_options)
            m.comments = form.cleaned_data["comments"]
            m.has_resource = len(options) > 0 or len(m.comments) > 0
            m.charge = form.cleaned_data["charge"]
            m.place_accessible = form.cleaned_data["place_accessible"]
            m.save()
            if resource_type == "offers":
                imageformset.save()
                for name in request.POST:
                    if name.startswith("delete-image-"):
                        name = name.removeprefix("delete-image-")
                        try:
                            image_id = int(name)
                            image = imagemodel.objects.get(pk=image_id)
                            if image.resource.organization != org:
                                continue
                            f = Path(image.image.path)
                            if f.is_file():
                                f.unlink()
                            image.delete()
                        except Exception:
                            raise

            return redirect_resource_set(org, resource_type, resource)
        else:
            return render_wizard(
                request,
                org,
                resource,
                form,
                resource_type,
                editing=editing,
                db_resource=m,
                imageforms=imageformset,
            )

    r, form = get_resource_form(org, resource_type, resource)
    return render_wizard(request, org, resource, form, resource_type, db_resource=r)


def redirect_resource_set(org, resource_type, resource):
    if org.resources_set:
        return redirect("app")

    next_resource = get_next_resource(resource)
    if next_resource is None:
        if resource_type == "needs":
            return redirect("mid-wizard", organization_id=org.id)
        else:
            return redirect_wizard_finish(org)

    return redirect(
        "resources-wizard",
        organization_id=org.id,
        resource_type=resource_type,
        resource=next_resource,
    )


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
        return posted_file  # exif will not work for files other than JPEG


@login_required
@require_own_organization
@record_stats("matches")
def matches(request, organization_id):
    # TODO better matches computation, does much more work than needed
    organization = get_object_or_404(Organization, pk=organization_id)
    own_needs = get_own_needs(organization)
    needs_json = [
        {
            "resource": x.resource,
            "options": [o.name for o in x.sorted_options()],
        }
        for x in own_needs
    ]
    offer_matches, need_matches = get_organization_matches(
        request.user, organization, own_needs
    )
    organization_matches = group_matches_by_organization(
        organization, offer_matches, need_matches
    )
    matches = {}
    for need in needs_json:
        need = need["resource"]
        matches[need] = [
            m.json(
                current_organization=organization,
                include_org=True,
            )
            for l in organization_matches
            for m in l
            if m.resource == need
        ]
    return render_matches_page(
        request, "femlliga/matches.html", organization, matches, needs_json
    )


def render_matches_page(
    request, template, organization, matches, needs_json, organization_matches=None
):
    matches = {k: v for k, v in matches.items() if len(v) > 0}
    json_data = {
        "matches": matches,
        "needs": needs_json,
        "resource_names_map": RESOURCE_NAMES_MAP,
        "option_names_map": RESOURCE_OPTIONS_DEF_MAP,
        "resource_icons_map": RESOURCE_ICONS_MAP,
    }
    if organization_matches:
        json_data["organization_matches"] = organization_matches

    return render(
        request,
        template,
        {
            "org": organization,
            "json_data": json_data,
            "wizard_finished": str_to_bool(request.GET.get("wizard_finished")),
        },
    )


def group_matches_by_organization(organization, offer_matches, need_matches):
    orgs = {}
    for k, l in offer_matches.items():
        for m in l:
            orgs.setdefault(m.organization.id, []).append(m)
    for k, l in need_matches.items():
        for m in l:
            orgs.setdefault(m.organization.id, []).append(m)

    return [
        orgs[k]
        for k in sorted(
            orgs.keys(), key=lambda k: orgs[k][0].organization.distance(organization)
        )
    ]


def get_organization_matches(user, organization, own_needs):
    offer_matches, need_matches = {}, {}
    for need in own_needs:
        need_options = [n.name for n in need.options.all()]
        offers = get_model_matches(
            user,
            organization,
            need.resource,
            Offer,
            need_options=need_options,
            include_other=False,
        )
        if len(offers) > 0:
            offer_matches[need.resource] = offers

        needs = get_model_matches(
            user,
            organization,
            need.resource,
            Need,
            need_options=need_options,
            include_other=False,
        )
        if len(needs) > 0:
            need_matches[need.resource] = needs

    return offer_matches, need_matches


def get_model_matches(
    user, organization, resource, model, need_options=None, include_other=True
):
    if need_options is None:
        queryset = model.objects.filter(
            resource=resource,
            has_resource=True,
        )
    else:
        queryset = model.objects.filter(
            resource=resource,
            has_resource=True,
            options__name__in=need_options,
        )

    if not include_other:
        queryset = queryset.exclude(resource="OTHER")

    # limit distance inside db so fewer results are retrieved
    queryset = limit_organizations_distance(
        queryset,
        organization,
        user.distance_limit_km,
        field_prefix="organization__",
    )
    results = (
        queryset.exclude(organization=organization)
        .prefetch_related("organization", "images", "options")
        .distinct()
    )
    # limit distance in python, so exactly the appropriate results are returned
    results = [
        r
        for r in results
        if r.organization.distance(organization) < user.distance_limit_km
    ]

    # add matches with announcements
    if model is Need:
        if need_options is None:
            queryset = Announcement.objects.filter(
                resource=resource,
                public=True,
            )
        else:
            queryset = Announcement.objects.filter(
                resource=resource,
                public=True,
                option__name__in=need_options,
            )

        queryset = limit_organizations_distance(
            queryset,
            organization,
            user.distance_limit_km,
            field_prefix="organization__",
        )
        results_2 = (
            queryset.exclude(organization=organization)
            .prefetch_related("organization", "option")
            .distinct()
        )
        for r in results_2:
            if r.organization.distance(organization) < user.distance_limit_km:
                results = add_announcement_result(results, r)

    return sorted(results, key=lambda r: r.organization.distance(organization))


def add_announcement_result(results, r):
    found = False
    for er in results:
        if er.resource == r.resource and er.organization == r.organization:
            found = True
            if hasattr(er, "announcements"):
                er.announcements.append(r)
            else:
                er.announcements = [r]
    if not found:
        results.append(r)
    return results


def get_all_resources(user, organization):
    offer_matches, need_matches = {}, {}
    for resource in RESOURCES:
        offers = get_model_matches(user, organization, resource[0], Offer)
        if len(offers) > 0:
            offer_matches[resource[0]] = offers

        needs = get_model_matches(user, organization, resource[0], Need)
        if len(needs) > 0:
            need_matches[resource[0]] = needs

    return offer_matches, need_matches


@login_required
@require_own_organization
@record_stats("search")
def search(request, organization_id):
    organization = organization_prefetches(
        request.user.organizations.filter(id=organization_id)
    ).first()
    offer_matches, need_matches = get_all_resources(request.user, organization)
    organization_matches = group_matches_by_organization(
        organization, offer_matches, need_matches
    )
    matches = {
        "offerMatches": {
            k: [
                m.json(
                    current_organization=organization,
                    include_org=True,
                )
                for m in offer_matches[k]
            ]
            for k in offer_matches
        },
        "needMatches": {
            k: [
                m.json(
                    current_organization=organization,
                    include_org=True,
                )
                for m in need_matches[k]
            ]
            for k in need_matches
        },
    }
    organization_matches = [
        {
            "organization": l[0].organization.json(current_organization=organization),
            "matches": [
                m.json(
                    current_organization=organization,
                    include_org=True,
                )
                for m in l
            ],
        }
        for l in organization_matches
    ]
    return render_matches_page(
        request,
        "femlliga/search.html",
        organization,
        matches,
        [x[0] for x in RESOURCES],
        organization_matches=organization_matches,
    )


@login_required
def preferences(request):
    form = PreferencesForm(model_to_dict(request.user))
    if request.method == "POST":
        form, ok, msg = save_preferences(request)
        if ok:
            messages.info(request, msg, extra_tags="show")
            return redirect("preferences")

    other_emails = EmailAddress.objects.filter(user=request.user).exclude(
        email=request.user.email
    )
    return render(
        request,
        "femlliga/preferences.html",
        {
            "form": form,
            "other_emails": [e for e in other_emails],
            "json_data": {
                "distance": request.user.distance_limit_km,
            },
        },
    )


def save_preferences(request):
    form = PreferencesForm(request.POST)
    if form.is_valid():
        new_email = clean_form_email(form.cleaned_data["email"])
        if new_email != request.user.email:
            if (
                EmailAddress.objects.filter(email=new_email)
                .exclude(user=request.user)
                .count()
                > 0
            ):
                form.add_error("email", _("Aquesta adreça ja està en ús"))
                form.cleaned_data["email"] = new_email
                return form, False, ""
            try:
                e = EmailAddress.objects.get(email=new_email, user=request.user)
                e.send_confirmation()
            except EmailAddress.DoesNotExist:
                # will send confirmation email and then execute
                # update_user_email function on email_confirmed signal
                EmailAddress.objects.add_email(
                    request, request.user, new_email, confirm=True
                )

        request.user.language = form.cleaned_data["language"]
        request.user.distance_limit_km = form.cleaned_data["distance_limit_km"]
        request.user.notifications_frequency = form.cleaned_data[
            "notifications_frequency"
        ]
        request.user.notify_immediate_communications_received = form.cleaned_data[
            "notify_immediate_communications_received"
        ]
        request.user.notify_immediate_announcement_communications_received = (
            form.cleaned_data["notify_immediate_announcement_communications_received"]
        )
        request.user.notify_agreement_communication_pending = form.cleaned_data[
            "notify_agreement_communication_pending"
        ]
        request.user.notify_matches = form.cleaned_data["notify_matches"]
        request.user.notify_new_resources = form.cleaned_data["notify_new_resources"]
        request.user.save()
        msg = _("La configuració s'ha desat correctament")
        if new_email != request.user.email:
            msg += _(". S'ha enviat un correu electrònic per confirmar la nova adreça")
        return form, True, msg
    return form, False, ""


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # set new address as primary
    email_address.set_as_primary()
    email_address.user.email = email_address.email
    email_address.user.save()
    # remove previous addresses
    EmailAddress.objects.filter(
        user=email_address.user,
    ).exclude(primary=True).delete()


@login_required
def discard_user_email(request, pk):
    address = get_object_or_404(EmailAddress, pk=pk)
    if address.user != request.user:
        raise PermissionDenied()

    if request.method == "POST":
        if address.primary:
            raise PermissionDenied()

        address.delete()
        return redirect("preferences")

    return render(request, "femlliga/discard_user_email.html", {"address": address})


@login_required
def delete_account(request):
    if request.method == "POST" and request.user.organizations.count() == 1:
        request.user.organizations.first().delete()
        request.user.delete()
        messages.info(
            request, _("S'ha esborrat el compte i l'organització"), extra_tags="show"
        )
        return redirect("index")

    return redirect("preferences")


@login_required
@require_own_organization
def send_message(request, organization_id, organization_to, resource_type, resource):
    if request.method != "POST":
        return JsonResponse({})

    assert_url_param_in_list(resource_type, ["need", "offer"])
    assert_url_param_in_list(resource, RESOURCES_LIST)
    organization = get_object_or_404(Organization, pk=organization_id)
    other = get_object_or_404(Organization, pk=organization_to)
    model = Offer if resource_type == "offer" else Need
    r = get_object_or_404(model, organization=other, resource=resource)
    post = get_json_body(request)
    form = MessageForm(post, resource=r)
    if form.is_valid():
        a = Agreement.objects.create(
            solicitor=organization,
            solicitee=other,
            message=form.cleaned_data["message"],
            origin=form.cleaned_data["origin"],
            resource=resource,
            resource_type=resource_type,
            communication_accepted=True,
            communication_date=timezone.now(),
        )
        for option in form.cleaned_data["options"]:
            # avoid clash with _ translation function
            ro, _created = ResourceOption.objects.get_or_create(name=option)
            a.options.add(ro)

        if other.creator.notify_immediate_communications_received:
            subject = _("T'han enviat una petició per intercanviar %(resource)s") % {
                "resource": resource_name(a.resource),
            }
            send_notification(
                user=other.creator,
                subject=subject,
                template="email/notify_communication_received.html",
                context={
                    "a": a,
                    "current_site": get_current_site(request),
                },
            )

        return JsonResponse(
            {
                "ok": True,
                "agreement_url": reverse(
                    "agreement",
                    kwargs={"organization_id": organization_id, "agreement_id": a.id},
                ),
            }
        )
    return JsonResponse({"ok": False})


@login_required
@require_own_organization
def agreements(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    sent = sort_agreements(
        organization.sent_agreements.all().prefetch_related(
            "messages", "options", "solicitee"
        )
    )
    received = sort_agreements(
        organization.received_agreements.all().prefetch_related(
            "messages", "options", "solicitee"
        )
    )
    agreements_by_organization = group_agreements_by_organizations(
        sort_agreements(sent + received), organization
    )
    organization_names_map_json = {}
    for agreements in agreements_by_organization:
        org = agreement_other_organization(agreements[0], organization_id)
        organization_names_map_json[str(org.id)] = org.name
    return render(
        request,
        "femlliga/agreements.html",
        {
            "org": organization,
            "agreements": {"sent": sent, "received": received},
            "json_data": {
                "agreements": {
                    "sent": group_agreements_by_resource_json(sent, organization_id),
                    "received": group_agreements_by_resource_json(
                        received, organization_id
                    ),
                },
                "concatenated_agreements": [
                    a.json(organization_id) for a in sort_agreements(sent + received)
                ],
                "resource_names_map": RESOURCE_NAMES_MAP,
                "option_names_map": RESOURCE_OPTIONS_DEF_MAP,
                "resource_icons_map": RESOURCE_ICONS_MAP,
                "organizations": [
                    {
                        "organization": agreement_other_organization(
                            l[0], organization_id
                        ).json(current_organization=organization),
                        "agreements": [a.json(organization_id) for a in l],
                    }
                    for l in agreements_by_organization
                ],
                "requested_resources": {
                    "sent": requested_resources(sent),
                    "received": requested_resources(received),
                },
            },
        },
    )


@login_required
@require_own_agreement
def agreement(request, organization_id, agreement_id):
    a = get_object_or_404(Agreement, pk=agreement_id)
    org = get_object_or_404(Organization, pk=organization_id)
    return render(
        request,
        "femlliga/agreement.html",
        {
            "a": a,
            "org": org,
            "json_data": {
                "agreement_id": a.id,
                "org_id": org.id,
                "messages": a.all_messages_json(),
            },
        },
    )


@login_required
@require_own_agreement
def view_agreement_email(request, organization_id, agreement_id):
    a = get_object_or_404(Agreement, pk=agreement_id)
    return render(
        request,
        "email/notify_communication_received.html",
        {
            "a": a,
            "current_site": get_current_site(request),
        },
    )


@login_required
@require_own_agreement
def send_agreement_message(request, organization_id, agreement_id):
    if request.method == "POST":
        a = get_object_or_404(Agreement, pk=agreement_id)
        org = get_object_or_404(Organization, pk=organization_id)
        message = request.POST.get("message", "")
        async_to_sync(create_agreement_message)(a, org, message)

    return redirect(
        "agreement", organization_id=organization_id, agreement_id=agreement_id
    )


@login_required
@require_own_agreement
def mark_message_read(request, organization_id, agreement_id, message_id):
    if request.method == "POST":
        m = get_object_or_404(Message, pk=message_id)
        if m.agreement != get_object_or_404(Agreement, pk=agreement_id):
            return JsonResponse({"ok": False})
        m.read = True
        m.save()

    return JsonResponse({"ok": True})


@login_required
@require_own_organization
def announcements(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    return render(
        request,
        "femlliga/announcements.html",
        {
            "org": organization,
            "json_data": {
                "org_id": str(organization.id),
                "resource_labels": NEEDS_PUBLISHABLE_OPTIONS_LABELS_MAP_2,
                "announcements": [
                    a.json()
                    for a in organization.announcements.all().prefetch_related(
                        "contacts", "option"
                    )
                ],
            },
        },
    )


@login_required
@require_own_organization
def add_announcement(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    form = AnnouncementForm()
    return edit_announcement_aux(request, organization, form)


@login_required
@require_own_organization
def edit_announcement(request, organization_id, announcement_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    form = AnnouncementForm(model_to_dict(announcement))
    return edit_announcement_aux(request, organization, form, announcement=announcement)


def edit_announcement_aux(request, organization, form, announcement=None):
    editing = announcement is not None
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ro, _created = ResourceOption.objects.get_or_create(
                name=form.cleaned_data["option"]
            )
            if not announcement:
                announcement = Announcement(organization=organization)
            announcement.public = form.cleaned_data["public"]
            announcement.title = form.cleaned_data["title"]
            announcement.description = form.cleaned_data["description"]
            announcement.resource = form.cleaned_data["resource"]
            announcement.option = ro
            announcement.save()
            if editing:
                return redirect(
                    "announcement",
                    organization_id=organization.id,
                    announcement_id=announcement.id,
                )
            return redirect("announcements", organization_id=organization.id)

    return render(
        request,
        "femlliga/add_announcement.html",
        {
            "form": form,
            "object": announcement,
            "json_data": {
                "resource_descriptions": NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP_2
            },
        },
    )


@login_required
@require_own_organization
def announcement(request, organization_id, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    if announcement.organization.id != organization_id:
        raise PermissionDenied()

    return render(
        request,
        "femlliga/announcement.html",
        {
            "announcement": announcement,
            "json_data": {
                "org_id": str(organization_id),
                "announcement_id": str(announcement_id),
                "contacts": [c.json() for c in announcement.contacts.all()],
            },
        },
    )


@login_required
@require_own_organization
def mark_announcement_contact_read(
    request, organization_id, announcement_id, contact_id
):
    if request.method == "POST":
        c = get_object_or_404(AnnouncementContact, pk=contact_id)
        if (
            c.announcement.id != announcement_id
            or c.announcement.organization.id != organization_id
        ):
            return JsonResponse({"ok": False})
        c.read = True
        c.save()

    return JsonResponse({"ok": True})


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

    return [
        orgs[k]
        for k in sorted(
            orgs.keys(),
            key=lambda k: agreement_other_organization(
                orgs[k][0], organization.id
            ).distance(organization),
        )
    ]


def agreement_other_organization(agreement, organization_id):
    if agreement.solicitor_safe().id == organization_id:
        return agreement.solicitee_safe()
    return agreement.solicitor_safe()


@login_required
@require_own_agreement
def agreement_successful(request, organization_id, agreement_id):
    if request.method == "POST":
        a = get_object_or_404(Agreement, pk=agreement_id)
        a.agreement_successful = request.POST.get("successful", "no") == "yes"
        a.successful_date = timezone.now()
        a.save()

    return redirect(
        "agreement", organization_id=organization_id, agreement_id=agreement_id
    )


def get_city_from_coordinates(lat, lng):
    """Nominatim also accepts a search option that gives coordinates given a place's name"""
    try:
        res = http_get(
            f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
        )
        try:
            return res["address"]["city"]
        except:
            return res["address"]["town"]
    except:
        return "Unknown city"


def organization_prefetches(queryset, include_missing_resources=False):
    if include_missing_resources:
        queryset = queryset.prefetch_related("needs", "offers")
    else:
        queryset = queryset.prefetch_related(
            Prefetch("needs", queryset=Need.objects.filter(has_resource=True)),
            Prefetch("offers", queryset=Offer.objects.filter(has_resource=True)),
        )
    return queryset.prefetch_related(
        "scopes",
        "social_media",
        "needs__options",
        "offers__options",
        "needs__images",
        "offers__images",
        "sent_agreements__options",
        "received_agreements__options",
    )


@user_passes_test(lambda u: u.is_staff)
def report(request):
    return report_aux(request)


def report_public(request):
    return report_aux(request, public=True)


def report_aux(request, public=False):
    active_tab = request.GET.get("tab")
    if request.method == "POST" and request.POST.get("delete_word"):
        ExcludeCommentWord.objects.create(value=request.POST.get("delete_word"))
        return redirect(reverse("report") + "?tab=comments")

    organizations = organization_prefetches(Organization.objects.all())
    needs = Need.objects.filter(has_resource=True).prefetch_related(
        "organization", "options"
    )
    offers = Offer.objects.filter(has_resource=True).prefetch_related(
        "organization", "options"
    )
    agreements = Agreement.objects.all().prefetch_related(
        "solicitor", "solicitee", "options"
    )
    resources_df = pd.DataFrame()
    organizations_df = pd.DataFrame()
    agreements_df = pd.DataFrame()
    form = ReportFilterForm(request.POST)
    resources_filtered_by_option = False
    report_statistics = get_report_statistics()
    if request.method == "POST":
        report_statistics.requests_count += 1
        report_statistics.save()

    if form.is_valid():
        if active_tab in ("map", "organizations"):
            organizations = filter_report_organizations(organizations, form)
            organizations_df = get_organizations_df(organizations, form)
        if active_tab in ("agreements",):
            agreements_df = get_agreements_df(agreements, form)
        if active_tab in ("resources",):
            filtered_needs, filtered_offers, resources_df = get_report_resources(
                needs, offers, form
            )

            if form.cleaned_data["resource_option"]:
                resources_filtered_by_option = True

    if public:
        active_tab = active_tab or "organizations"
    else:
        active_tab = active_tab or "map"
    context = {
        "public": public,
        "active_tab": active_tab,
        "active_form": form,
        "inactive_form": ReportFilterForm(),
        "organizations": organizations,
        "organizations_df": organizations_df,
        "agreements_df": agreements_df,
        "resources_df": resources_df,
        "comment_word_counts": report_comments(needs, offers),
        "excluded_words": ", ".join(
            sorted([x.value for x in ExcludeCommentWord.objects.all()])
        ),
        "report_statistics": report_statistics,
        "json_data": {
            "organizations": [
                {"name": o.name, "lat": float(o.lat), "lng": float(o.lng)}
                for o in organizations
            ],
        },
    }
    if resources_filtered_by_option:
        context["filtered_resources_comment_word_counts"] = report_comments(
            filtered_needs, filtered_offers
        )
        context["needs_comments"] = [x.comments for x in filtered_needs if x.comments]
        context["offers_comments"] = [x.comments for x in filtered_offers if x.comments]

    return render(request, "femlliga/report.html", context)


def filter_report_organizations(organizations, form):
    filters = [
        ("province", lambda v, o: v == o.get_province()["id"]),
        ("org_type", lambda v, o: v == o.org_type),
        ("org_scope", lambda v, o: v in {s.name for s in o.scopes.all()}),
        ("start_date", lambda v, o: o.date >= date_to_datetime(v)),
        ("end_date", lambda v, o: o.date <= date_to_datetime(v)),
    ]
    for f in filters:
        value = form.cleaned_data.get(f[0])
        if value:
            organizations = [o for o in organizations if f[1](value, o)]

    return organizations


def get_report_resources(n, o, form):
    n, o = filter_report_resources(n, o, form)

    # n and o are needs and offers
    index, rows = [], []
    group_by = form.cleaned_data.get("group_resources_by")
    groups = [
        ("ORG_TYPE", ORG_TYPES, same_org_type),
        ("ORG_SCOPE", ORG_SCOPES, org_has_scope),
        ("RESOURCE", RESOURCES, same_resource),
        ("RESOURCE_OPTION", RESOURCE_OPTIONS_WITH_PREFIX, has_option),
    ]
    for g in groups:
        if group_by == g[0]:
            index, rows = group_report_resources(g[1], n, o, g[2])

    df = pd.DataFrame(
        rows,
        columns=[_("Necessitats"), _("Oferiments")],
        index=index,
    )

    if form.cleaned_data.get("hide_zeroes"):
        return n, o, df.loc[~(df == 0).all(axis=1)]

    if form.cleaned_data.get("show_only_zeroes"):
        return n, o, df.loc[(df == 0).all(axis=1)]

    return n, o, df


def get_organizations_df(organizations, form):
    index, rows = [], []
    group_by = form.cleaned_data.get("group_orgs_by")
    groups = [
        ("ORG_TYPE", ORG_TYPES, lambda org_type: lambda o: o.org_type == org_type),
        (
            "ORG_SCOPE",
            ORG_SCOPES,
            lambda org_scope: lambda o: org_scope in {s.name for s in o.scopes.all()},
        ),
    ]
    for g in groups:
        if group_by == g[0]:
            index, rows = group_organizations(g[1], organizations, g[2])

    df = pd.DataFrame(
        rows,
        columns=[str(_("Organitzacions"))],
        index=index,
    )

    if form.cleaned_data.get("hide_zeroes"):
        return df.loc[~(df == 0).all(axis=1)]

    if form.cleaned_data.get("show_only_zeroes"):
        return df.loc[(df == 0).all(axis=1)]

    return df


def filter_report_resources(needs, offers, form):
    filters = [
        ("province", lambda pr: lambda x: pr == x.organization.get_province()["id"]),
        ("org_type", same_org_type),
        ("org_scope", org_has_scope),
        ("resource", same_resource),
        ("resource_option", has_option),
        ("charge", offer_charges),
        ("start_date", lambda d: lambda x: x.last_updated_on >= date_to_datetime(d)),
        ("end_date", lambda d: lambda x: x.last_updated_on <= date_to_datetime(d)),
    ]
    for f in filters:
        value = form.cleaned_data.get(f[0])
        if value:
            needs = [x for x in needs if f[1](value)(x)]
            offers = [x for x in offers if f[1](value)(x)]

    return needs, offers


def get_agreements_df(agreements, form):
    agreements = filter_report_agreements(agreements, form)
    index, rows = [], []
    group_by = form.cleaned_data.get("group_agreements_by")
    groups = [
        (
            "SOLICITOR_ORG_TYPE",
            ORG_TYPES,
            lambda org_type: lambda a: a.solicitor and a.solicitor.org_type == org_type,
        ),
        (
            "SOLICITOR_ORG_SCOPE",
            ORG_SCOPES,
            lambda org_scope: lambda a: a.solicitor
            and org_scope in {s.name for s in a.solicitor.scopes.all()},
        ),
        (
            "SOLICITEE_ORG_TYPE",
            ORG_TYPES,
            lambda org_type: lambda a: a.solicitee and a.solicitee.org_type == org_type,
        ),
        (
            "SOLICITEE_ORG_SCOPE",
            ORG_SCOPES,
            lambda org_scope: lambda a: a.solicitee
            and org_scope in {s.name for s in a.solicitee.scopes.all()},
        ),
        ("RESOURCE", RESOURCES, same_resource),
        ("RESOURCE_OPTION", RESOURCE_OPTIONS_WITH_PREFIX, has_option),
        (
            "RESOURCE_TYPE",
            [("need", _("Necessitat")), ("offer", _("Oferiment"))],
            lambda rt: lambda a: a.resource_type == rt,
        ),
    ]
    for g in groups:
        if group_by == g[0]:
            index, rows = group_agreements(g[1], agreements, g[2])

    df = pd.DataFrame(
        rows,
        columns=[
            _("Peticions pendents"),
            _("Peticions sense acord"),
            _("Peticions amb acord"),
        ],
        index=index,
    )

    if form.cleaned_data.get("hide_zeroes"):
        return df.loc[~(df == 0).all(axis=1)]

    if form.cleaned_data.get("show_only_zeroes"):
        return df.loc[(df == 0).all(axis=1)]

    return df


def filter_report_agreements(agreements, form):
    filters = [
        (
            "solicitor_province",
            lambda v, a: a.solicitor and v == a.solicitor.get_province()["id"],
        ),
        (
            "solicitee_province",
            lambda v, a: a.solicitee and v == a.solicitee.get_province()["id"],
        ),
        ("solicitor_org_type", lambda v, a: a.solicitor and v == a.solicitor.org_type),
        ("solicitee_org_type", lambda v, a: a.solicitee and v == a.solicitee.org_type),
        (
            "solicitor_org_scope",
            lambda v, a: a.solicitor
            and v in {s.name for s in a.solicitor.scopes.all()},
        ),
        (
            "solicitee_org_scope",
            lambda v, a: a.solicitee
            and v in {s.name for s in a.solicitee.scopes.all()},
        ),
        ("resource", lambda v, a: v == a.resource),
        ("resource_option", lambda v, a: v in {x.name for x in a.options.all()}),
        ("communication_start_date", lambda v, a: a.date >= date_to_datetime(v)),
        ("communication_end_date", lambda v, a: a.date <= date_to_datetime(v)),
        (
            "agreement_start_date",
            lambda v, a: a.successful_date and a.successful_date >= date_to_datetime(v),
        ),
        (
            "agreement_end_date",
            lambda v, a: a.successful_date and a.successful_date <= date_to_datetime(v),
        ),
    ]
    for f in filters:
        value = form.cleaned_data.get(f[0])
        if value:
            agreements = [a for a in agreements if f[1](value, a)]

    return agreements


def same_org_type(org_type):
    return lambda x: org_type == x.organization.org_type


def same_resource(resource):
    return lambda x: resource == x.resource


def org_has_scope(scope):
    return lambda x: scope in {s.name for s in x.organization.scopes.all()}


def has_option(option):
    return lambda x: option in {o.name for o in x.options.all()}


def offer_charges(charges):
    if not charges:
        return lambda x: True

    def f(x):
        if not hasattr(x, "charge"):
            return True

        if (charges == "CHARGE" and x.charge) or (
            charges == "NO_CHARGE" and not x.charge
        ):
            return True

        return False

    return f


def group_report_resources(index, needs, offers, condition):
    rows = [
        (
            len([x for x in needs if condition(i[0])(x)]),
            len([x for x in offers if condition(i[0])(x)]),
        )
        for i in index
    ]
    return [str(x[1]) for x in index], rows


def group_organizations(index, organizations, condition):
    rows = [(len([x for x in organizations if condition(i[0])(x)]),) for i in index]
    return [str(x[1]) for x in index], rows


def group_agreements(index, agreements, condition):
    rows = [
        (
            len(
                [
                    x
                    for x in agreements
                    if condition(i[0])(x) and x.agreement_successful is None
                ]
            ),
            len(
                [
                    x
                    for x in agreements
                    if condition(i[0])(x) and x.agreement_successful is False
                ]
            ),
            len(
                [
                    x
                    for x in agreements
                    if condition(i[0])(x) and x.agreement_successful is True
                ]
            ),
        )
        for i in index
    ]
    return [str(x[1]) for x in index], rows


def report_comments(needs, offers):
    need_comments = " ".join([x.comments for x in needs if x.comments])
    offer_comments = " ".join([x.comments for x in offers if x.comments])
    comments = sanitize_for_searching(need_comments + " " + offer_comments).split()
    for w in ExcludeCommentWord.objects.all():
        comments = [c for c in comments if c != w.value]
    return collections.Counter(comments)


def sanitize_for_searching(s):
    return strip_accents(s.casefold()).replace(".", "").replace(",", "")


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def contact(request):
    if request.method != "POST":
        return render(request, "femlliga/contact.html", {"form": ContactForm()})

    form = ContactForm(request.POST)
    form_sent = False
    if form.is_valid():
        email = form.cleaned_data["email"]
        content = form.cleaned_data["content"]
        if ContactDenyList.objects.filter(email=clean_form_email(email)).count() > 0:
            logging.warning(f"Ignoring SPAM message from {email}")
            return render(
                request,
                "femlliga/contact.html",
                {"form": ContactForm(), "form_sent": True},
            )

        Contact(
            email=email,
            content=content,
        ).save()
        # send contact to managers
        mail_managers(
            _("S'ha rebut un contacte a la web de %(name)s")
            % {"name": get_current_site(request).name},
            _("Des del correu %(email)s envien el següent missatge:\n\n%(content)s")
            % {"email": email, "content": content},
        )

        # send confirmation to user
        subject = _(
            "El formulari de contacte amb %(name)s s'ha enviat correctament"
        ) % {
            "name": get_current_site(request).name,
        }
        send_email(
            to=[email],
            subject=subject,
            body=render_to_string(
                "email/contact_received.html",
                {
                    "content": content,
                    "current_site": get_current_site(request),
                },
            ),
        )
        form_sent = True
    return render(
        request, "femlliga/contact.html", {"form": form, "form_sent": form_sent}
    )


def maps(request):
    # novel functionality, only available in dev
    if not STAGING_ENVIRONMENT_NAME:
        raise PermissionDenied()

    orgs, maps = [], [
        {
            "name": "Fem lliga!",
            "code": "femlliga",
            "color": "gold",
            "orgs": get_femlliga_organizations(),
        },
        {
            "name": "Tornallom",
            "code": "tornallom",
            "color": "orange",
            "orgs": get_tornallom_organizations(),
        },
    ]

    for m in maps:
        m["count"] = len(m["orgs"])
        orgs += m["orgs"]
        del m["orgs"]

    return render(
        request,
        "femlliga/maps.html",
        {
            "maps": maps,
            "json_data": {"organizations": orgs, "maps": maps},
        },
    )


def public_announcements(request):
    announcements = Announcement.objects.filter(public=True)
    return render(
        request,
        "femlliga/public_announcements.html",
        {
            "provinces": sorted(
                [
                    (p["properties"]["id"], p["properties"]["name"])
                    for p in spain_provinces["features"]
                ],
                key=lambda p: strip_accents(p[1]),
            ),
            "json_data": {
                "announcements": [a.json(include_org=True) for a in announcements],
            },
        },
    )


def public_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not announcement.public:
        raise PermissionDenied()

    form = AnnouncementContactForm()
    if request.method == "POST":
        form = AnnouncementContactForm(request.POST)
        if form.is_valid():
            org = announcement.organization
            ec = AnnouncementContact.objects.create(
                announcement=announcement,
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )

            subject = _("S'ha enviat el següent missatge a «%(name)s»") % {
                "name": org.name
            }
            body = render_to_string(
                "email/announcement_contact_sent.html",
                {
                    "org": org,
                    "option": announcement.option,
                    "message": ec.message,
                    "current_site": get_current_site(request),
                },
            )
            send_email(to=[ec.email], subject=subject, body=body)

            if org.creator.notify_immediate_announcement_communications_received:
                subject = _("T'han contactat per una necessitat publicada")
                send_notification(
                    user=org.creator,
                    subject=subject,
                    template="email/notify_announcement_communication_received.html",
                    context={
                        "org": org,
                        "contact": ec,
                        "option": announcement.option,
                        "current_site": get_current_site(request),
                    },
                )

            msg = _(
                "S'ha enviat el missatge. L'organització es posarà en contacte amb tu el més aviat possible"
            )
            messages.info(request, msg, extra_tags="show")
            return redirect(reverse("public_announcement", args=[pk]))

    return render(
        request,
        "femlliga/public_announcement.html",
        {
            "form": form,
            "announcement": announcement,
            "json_data": {
                "sending": request.method == "POST",
            },
        },
    )


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
    def f(a):
        a_date = a.date
        a_messages = list(a.messages.all())
        if len(a_messages) > 0:
            a_date = a_messages[-1].sent_on
        return a_date

    return sorted(agreements, key=f, reverse=True)
