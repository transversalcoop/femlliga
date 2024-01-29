import json
import unicodedata

from datetime import timedelta
from distutils.util import strtobool

from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from femlliga.models import Organization, Agreement, Need, Offer
from femlliga.constants import FROM_EMAIL, RESOURCES, RESOURCES_ORDER, RESOURCE_OPTIONS_MAP, RESOURCE_OPTIONS_READABLE_MAP

# Emails and notifications

def get_users_to_notify():
    users = get_user_model().objects.exclude(notifications_frequency="NEVER")
    return [u for u in users if user_ready_to_notify(u)]

def user_ready_to_notify(user):
    time_from_last_notification = timezone.now() - user.last_notification_date
    return (user.notifications_frequency == "WEEKLY" and time_from_last_notification > timedelta(hours=7*24-1)) or \
        (user.notifications_frequency == "DAILY" and time_from_last_notification > timedelta(hours=23)) or \
        (user.notifications_frequency == "MONTHLY" and time_from_last_notification > timedelta(days=29, hours=23))

EMAIL_ITEMS_LIMIT = 3
def get_periodic_notification_data(site, user, needs, offers):
    context = {}

    org = Organization.objects.get(creator = user)
    if user.notify_agreement_communication_pending:
        pa = org_pending_agreements(org)
        if len(pa) > 0:
            context["agreement_communication_pending"] = {
                "agreements": pa[:EMAIL_ITEMS_LIMIT],
                "total_agreements": len(pa),
            }

    if user.notify_agreement_success_pending:
        pa = org_pending_success_agreements(org)
        if len(pa) > 0:
            context["agreement_success_pending"] = {
                "organization": org,
                "agreements": pa[:EMAIL_ITEMS_LIMIT],
                "total_agreements": len(pa),
            }

    time_from_last_long_notification = timezone.now() - user.last_long_notification_date
    long_notification_ready = time_from_last_long_notification > timedelta(days = 30 * 6)
    send_long_notification = False
    if user.notify_matches and long_notification_ready:
        # TODO FL090 consider only matches within distance_limit_km
        _, need, offer = user_has_matches(user, needs, offers)
        if need["count"] > 0 or offer["count"] > 0:
            context["matches"] = { "need": need, "offer": offer }
            send_long_notification = True

    # TODO FL078 (here and in periodic_notification.html)consider only resources with last_updated_on > last_long_notification_date
    # TODO FL090 consider only resources within distance_limit_km
    if user.notify_new_resources and long_notification_ready:
        if False:
            context["new_resources"] = {}
            send_long_notification = True

    if context:
        context["current_site"] = site
        context["send_long_notification"] = send_long_notification

    return context

def org_pending_agreements(o):
    try:
        a = Agreement.objects.filter(solicitee = o, communication_accepted = None)
        return list(a)
    except:
        return []

def org_pending_success_agreements(o):
    try:
        a = Agreement.objects.filter(
            Q(solicitee = o) | Q(solicitor = o),
            communication_accepted = True,
            agreement_successful = None,
        )
        return list(a)
    except:
        return []

def get_ordered_needs_and_offers():
    organizations = Organization.objects.all()
    all_needs, all_offers = [], []
    for resource in RESOURCES_ORDER:
        for option in RESOURCE_OPTIONS_MAP[resource]:
            needs, offers = [], []
            for o in organizations:
                for x in o.needs.all():
                    if x.has_resource == True and x.resource == resource and option[0] in [op.name for op in x.options.all()]:
                        needs.append(x)
                for x in o.offers.all():
                    if x.has_resource == True and x.resource == resource and option[0] in [op.name for op in x.options.all()]:
                        offers.append(x)
            all_needs.append((resource, option[0], len(needs)))
            all_offers.append((resource, option[0], len(offers)))

    return sorted(all_needs, key=lambda x: -x[2]), sorted(all_offers, key=lambda x: -x[2])

def user_has_matches(user, needs, offers):
    need, offer = {"name": "", "count": 0}, {"name": "", "count": 0}
    try:
        org = Organization.objects.get(creator=user)
    except:
        return None, need, offer

    for n in needs:
        if user_has_resource(Need, org, n):
            need = {"name": RESOURCE_OPTIONS_READABLE_MAP[(n[0], n[1])], "count": n[2]}
            break

    for o in offers:
        if user_has_resource(Offer, org, o):
            offer = {"name": RESOURCE_OPTIONS_READABLE_MAP[(o[0], o[1])], "count": o[2]}
            break

    return org, need, offer

def user_has_resource(model, org, n):
    return len(model.objects.filter(organization=org, resource=n[0], options=n[1], has_resource=True)) > 0

def send_notification(subject, template, user, context):
    send_email(to = [user.email], subject = subject, body = render_to_string(template, context))

def send_periodic_notification(subject, template, user, context):
    if not user_ready_to_notify(user):
        return False

    send_email(to = [user.email], subject = subject, body = render_to_string(template, context))

    user.last_notification_date = timezone.now()
    if context.get("send_long_notification", False):
        user.last_long_notification_date = timezone.now()
    user.save()

    return True

def send_email(to, subject, body):
    msg = EmailMessage(subject=subject, body=body, from_email=FROM_EMAIL, to=to)
    msg.content_subtype = "html"
    msg.send()

# Other

def wizard_url(o_id, index):
    resource_type = "needs"
    if index > len(RESOURCES):
        resource_type = "offers"
        index -= len(RESOURCES)
    resource = RESOURCES[index-1][0]
    return reverse("resources-wizard", kwargs={"organization_id": o_id, "resource_type": resource_type, "resource": resource})

def get_next_resource(resource):
    try:
        for i in range(len(RESOURCES)):
            if resource == RESOURCES[i][0]:
                return RESOURCES[i+1][0]
    except:
        return None

def get_resource_index(resource_type, resource):
    for i in range(len(RESOURCES)):
        if resource == RESOURCES[i][0]:
            if resource_type == "needs":
                return i+1
            return i+6
    return 0

def get_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8")) # request from Javascript's fetch API
    except:
        return request.POST # request from Django, or test

def str_to_bool(s):
    if not s:
        return False
    return bool(strtobool(s))

def clean_form_email(s):
    return unicodedata.normalize("NFKC", s.strip()).casefold()
