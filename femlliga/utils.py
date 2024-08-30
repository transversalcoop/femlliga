import json
import urllib
import decimal
import unicodedata

from datetime import timedelta
from operator import attrgetter
from functools import wraps
from distutils.util import strtobool

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models import F, Func, Q
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site

from shapely.geometry import shape, Point

from femlliga.constants import (
    FROM_EMAIL,
    RESOURCE_OPTIONS_MAP,
    RESOURCE_OPTIONS_READABLE_MAP,
    RESOURCES,
    RESOURCES_ORDER,
)
from femlliga.models import (
    Agreement,
    EmailSent,
    Message,
    Need,
    Offer,
    Organization,
    sort_resources,
)

from femlliga.gis.es import spain_provinces

# Emails and notifications


def get_users_to_notify():
    users = get_user_model().objects.exclude(notifications_frequency="NEVER")
    return [u for u in users if u.organizations.count() > 0 and user_ready_to_notify(u)]


def user_ready_to_notify(user):
    time_from_last_notification = timezone.now() - user.last_notification_date
    return (
        (
            user.notifications_frequency == "WEEKLY"
            and time_from_last_notification > timedelta(hours=7 * 24 - 1)
        )
        or (
            user.notifications_frequency == "DAILY"
            and time_from_last_notification > timedelta(hours=23)
        )
        or (
            user.notifications_frequency == "MONTHLY"
            and time_from_last_notification > timedelta(days=29, hours=23)
        )
    )


EMAIL_ITEMS_LIMIT = 3


def get_periodic_notification_data(site, user, needs, offers):
    context = {}

    org = Organization.objects.get(creator=user)
    if user.notify_agreement_communication_pending:
        pa = org_pending_agreements(org)
        if len(pa) > 0:
            context["agreement_communication_pending"] = {
                "agreements": pa[:EMAIL_ITEMS_LIMIT],
                "total_agreements": len(pa),
            }

    time_from_last_long_notification = timezone.now() - user.last_long_notification_date
    long_notification_ready = time_from_last_long_notification > timedelta(days=30 * 6)
    send_long_notification = False
    if user.notify_matches and long_notification_ready:
        _, need, offer = org_has_matches(org, needs, offers)
        if need["count"] > 0 or offer["count"] > 0:
            context["matches"] = {"need": need, "offer": offer}
            send_long_notification = True

    if user.notify_new_resources and long_notification_ready:
        offers = org_offers_not_matching(org, user)
        if len(offers) > 0:
            context["new_resources"] = {"resources": offers}
            send_long_notification = True

    if context:
        context["current_site"] = site
        context["send_long_notification"] = send_long_notification

    return context


def org_pending_agreements(o):
    try:
        agreements = Agreement.objects.filter(
            solicitee=o, communication_accepted=True, agreement_successful=None
        )
        return [
            a
            for a in agreements
            if a.messages.count() == 0 or a.messages.last().sent_by != o
        ]
    except:
        return []


def limit_organizations_distance(queryset, organization, max_distance, field_prefix=""):
    # 111.22 is approximate number of km in a lat or lng degree
    max_degree = max_distance / decimal.Decimal(111.22)
    # if delta is the angle difference in degrees
    # abs(delta) must be less than max_distance/km_in_degree
    return (
        queryset.annotate(
            lat_delta=Func(F(field_prefix + "lat") - organization.lat, function="ABS")
        )
        .annotate(
            lng_delta=Func(F(field_prefix + "lng") - organization.lng, function="ABS")
        )
        .exclude(lat_delta__gt=max_degree)
        .exclude(lng_delta__gt=max_degree)
    )


def get_ordered_needs_and_offers(org, distance_limit_km):
    organizations = limit_organizations_distance(
        Organization.objects.exclude(id=org.id), org, distance_limit_km
    )
    all_needs, all_offers = [], []
    for resource in RESOURCES_ORDER:
        for option in RESOURCE_OPTIONS_MAP[resource]:
            needs, offers = [], []
            for o in organizations:
                for x in o.needs.all():
                    if (
                        x.has_resource == True
                        and x.resource == resource
                        and option[0] in [op.name for op in x.options.all()]
                    ):
                        needs.append(x)
                for x in o.offers.all():
                    if (
                        x.has_resource == True
                        and x.resource == resource
                        and option[0] in [op.name for op in x.options.all()]
                    ):
                        offers.append(x)
            all_needs.append((resource, option[0], len(needs)))
            all_offers.append((resource, option[0], len(offers)))

    return sorted(all_needs, key=lambda x: -x[2]), sorted(
        all_offers, key=lambda x: -x[2]
    )


def org_has_matches(org, needs, offers):
    need, offer = {"name": "", "count": 0}, {"name": "", "count": 0}
    for n in needs:
        if org_has_resource(Need, org, n):
            need = {"name": RESOURCE_OPTIONS_READABLE_MAP[(n[0], n[1])], "count": n[2]}
            break

    for o in offers:
        if org_has_resource(Need, org, o):
            offer = {"name": RESOURCE_OPTIONS_READABLE_MAP[(o[0], o[1])], "count": o[2]}
            break

    return org, need, offer


def org_offers_not_matching(org, user):
    offers = []
    own_needs = get_own_needs(org)
    for need in own_needs:
        need_options = [n.name for n in need.options.all()]
        queryset = Offer.objects.exclude(organization=org).filter(
            resource=need.resource,
            has_resource=True,
            last_updated_on__gt=user.last_long_notification_date,
        )
        queryset = limit_organizations_distance(
            queryset,
            org,
            user.distance_limit_km,
            field_prefix="organization__",
        )
        l = list(queryset)
        l = [o for o in l if has_different_options(o.options.all(), need_options)]
        if len(l) > 0:
            offers.append(join_offers_not_matching(l, need_options))

    return offers


def has_different_options(has_options, exclude_options):
    return any([o.name not in exclude_options for o in has_options])


def join_offers_not_matching(offers, ignore_options):
    options = set()
    for offer in offers:
        for o in offer.options.all():
            if o.name not in ignore_options:
                options.add(o)
    return {
        "code": offers[0].resource,
        "options": list(sorted(options, key=lambda x: str(x))),
    }


def get_own_needs(org):
    return sort_resources(
        [
            n
            for n in org.needs.all().prefetch_related("options")
            if n.has_resource and n.resource != "OTHER"
        ]
    )


def org_has_resource(model, org, n):
    return (
        len(
            model.objects.filter(
                organization=org, resource=n[0], options=n[1], has_resource=True
            )
        )
        > 0
    )


def send_notification(subject, template, user, context):
    send_email(
        to=[user.email], subject=subject, body=render_to_string(template, context)
    )


def send_periodic_notification(subject, template, user, context):
    if not user_ready_to_notify(user):
        return False

    send_email(
        to=[user.email], subject=subject, body=render_to_string(template, context)
    )

    user.last_notification_date = timezone.now()
    if context.get("send_long_notification", False):
        user.last_long_notification_date = timezone.now()
    user.save()

    return True


def send_welcome_email(org):
    send_email(
        to=[org.creator.email],
        subject=_("Benvingudes a Fem lliga!"),
        body=render_to_string(
            "email/welcome.html",
            {
                "org": org,
                "current_site": Site.objects.get(id=settings.SITE_ID),
            },
        ),
        attachments=["static/segell-fem-lliga.png"],
    )
    org.welcome_email_sent = True
    org.save()


def send_email(to, subject, body, attachments=None):
    msg = EmailMessage(subject=subject, body=body, from_email=FROM_EMAIL, to=to)
    if attachments:
        for att in attachments:
            msg.attach_file(att)
    msg.content_subtype = "html"
    msg.send()

    try:
        sent_to = ",".join(to)
    except:
        sent_to = str(to)
    EmailSent.objects.create(sent_to=sent_to, subject=subject, body=body)


# Other


def wizard_url(o_id, index):
    resource_type = "needs"
    if index > len(RESOURCES):
        resource_type = "offers"
        index -= len(RESOURCES)
    resource = RESOURCES[index - 1][0]
    return reverse(
        "resources-wizard",
        kwargs={
            "organization_id": o_id,
            "resource_type": resource_type,
            "resource": resource,
        },
    )


def get_next_resource(resource):
    try:
        for i in range(len(RESOURCES)):
            if resource == RESOURCES[i][0]:
                return RESOURCES[i + 1][0]
    except:
        return None


def get_resource_index(resource_type, resource):
    for i in range(len(RESOURCES)):
        if resource == RESOURCES[i][0]:
            if resource_type == "needs":
                return i + 1
            return i + len(RESOURCES) + 1
    return 0


def get_json_body(request):
    try:
        return json.loads(
            request.body.decode("utf-8")
        )  # request from Javascript's fetch API
    except:
        return request.POST  # request from Django, or test


def str_to_bool(s):
    if not s:
        return False
    return bool(strtobool(s))


def clean_form_email(s):
    return unicodedata.normalize("NFKC", s.strip()).casefold()


def http_get(url):
    with urllib.request.urlopen(url) as f:
        res = json.loads(f.read().decode("utf-8"))
    return res


def cache(timedelta):
    def decorator(func):
        value = None
        last_execution = None

        @wraps(func)
        def decorated():
            nonlocal value
            nonlocal last_execution

            # first execution, must call func
            if value is None:
                value = func()
                last_execution = timezone.now()
                return value

            # value outdated, update it, but if it fails, use old value
            if (timezone.now() - last_execution) > timedelta:
                try:
                    value = func()
                    last_execution = timezone.now()
                    return value
                except:
                    return value

            # value cached
            return value

        return decorated

    return decorator


async def create_agreement_message(agreement, organization, message):
    if not message or agreement.agreement_successful is not None:
        return

    m = await Message.objects.acreate(
        sent_by=organization,
        message=message,
        agreement=agreement,
    )
    return m


def truncate(s):
    parts = s.split(" ")
    n = 50
    if len(parts) > n:
        return " ".join(parts[:n]) + "..."
    return s


def get_province(lat, lng, features):
    p = Point(lng, lat)
    for feature in features:
        polygon = shape(feature["geometry"])
        if polygon.contains(p):
            return feature["properties"]
    return {"id": ""}


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


spain_provinces_choices = sorted(
    [
        (f["properties"]["id"], f["properties"]["name"])
        for f in spain_provinces["features"]
    ],
    key=lambda x: strip_accents(x[1]),
)


def date_to_datetime(d):
    return timezone.make_aware(timezone.datetime(d.year, d.month, d.day))
