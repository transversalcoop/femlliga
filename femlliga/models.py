import base64
import math
import unicodedata
import uuid
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from . import constants as const


def add_one_month(t):
    t = t.replace(day=1)
    t = t + timedelta(days=32)
    t = t.replace(day=1)
    return t


def add_days(days):
    def f(t):
        return t + timedelta(days=days)

    return f


def date_intervals(start, end):
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    if (end - start) < timedelta(days=30):
        f = add_days(1)
    elif (end - start) < timedelta(days=30 * 3):
        f = add_days(7)
    else:
        start = start.replace(day=1)
        f = add_one_month

    intervals = [start]
    mid = start
    while mid < end:
        mid = f(mid)
        intervals.append(mid)

    return intervals


def clean_form_email(s):
    return unicodedata.normalize("NFKC", s.strip()).casefold()


def need_images_directory_path(instance, filename):
    return str(Path("images/needs") / filename)


def offer_images_directory_path(instance, filename):
    return str(Path("images/offers") / filename)


def organization_logos_directory_path(instance, filename):
    return str(Path("images/logos") / filename)


@deconstructible
class LimitFileSize:
    def __init__(self, MB):
        self.MB = MB
        self.limit = MB * 1024 * 1024

    def __call__(self, value):
        if value.size > self.limit:
            raise ValidationError(
                _(
                    "L'arxiu és massa gran, hauria d'ocupar menys de %(max)s MB.",
                    max=self.MB,
                )
            )

    def __eq__(self, other):
        return self.MB == other.MB


USER_LANGUAGE_CHOICES = [("", _("Idioma configurat al navegador"))] + [
    x for x in const.LANGUAGE_CHOICES
]


class CustomUser(AbstractUser):
    language = models.CharField(
        max_length=50, choices=USER_LANGUAGE_CHOICES, null=True, blank=True
    )
    distance_limit_km = models.DecimalField(
        max_digits=6, decimal_places=1, default=100
    )  # from 0.0 to 99999.9

    # immediate notifications
    # DEPRECATED
    accept_communications_automatically = models.BooleanField(default=True)
    notify_immediate_communications_received = models.BooleanField(default=True)
    notify_immediate_announcement_communications_received = models.BooleanField(
        default=True
    )
    # DEPRECATED
    notify_immediate_communications_rejected = models.BooleanField(default=True)

    # periodic notifications
    last_notification_date = models.DateTimeField(auto_now_add=True)
    last_long_notification_date = models.DateTimeField(auto_now_add=True)
    notifications_frequency = models.CharField(
        max_length=50, choices=const.NOTIFICATION_CHOICES, default="WEEKLY"
    )
    notify_agreement_communication_pending = models.BooleanField(default=True)
    # DEPRECATED
    notify_agreement_success_pending = models.BooleanField(default=True)
    notify_matches = models.BooleanField(default=True)
    notify_new_resources = models.BooleanField(default=True)

    def get_organization(self):
        organizations = self.organizations.all()
        if len(organizations) > 0:
            return organizations[0]
        return None


class Page(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    name = models.SlugField()
    language = models.CharField(
        max_length=50, choices=const.LANGUAGE_CHOICES, default="ca"
    )
    heading = models.TextField()
    subheading = models.TextField(blank=True)
    content = models.TextField()
    image = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (("name", "language"),)
        verbose_name = _("Pàgina")
        verbose_name_plural = _("Pàgines")

    def __str__(self):
        return f"[{self.language}] {self.name}"


class OrganizationScope(models.Model):
    name = models.CharField(max_length=100, choices=const.ORG_SCOPES, primary_key=True)

    def __str__(self):
        return str(const.ORG_SCOPES_NAMES_MAP[self.name])


class Organization(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to=organization_logos_directory_path,
        validators=[LimitFileSize(10)],
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    scopes = models.ManyToManyField(OrganizationScope)
    org_type = models.CharField(max_length=100, choices=const.ORG_TYPES)
    resources_set = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=12, decimal_places=9)
    lng = models.DecimalField(max_digits=12, decimal_places=9)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="organizations",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Organització")
        verbose_name_plural = _("Organitzacions")

    def __str__(self):
        return self.name

    @classmethod
    def deleted_organization(cls):
        o = Organization(name=_("«organització eliminada»"), lat=0, lng=0)
        o.id = None  # even if an id is not given, the constructor creates it
        return o

    def json(self, current_organization=None, include_children=False):
        j = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "org_type": self.org_type,
        }
        # could be a deleted organization
        if self.id:
            j["href"] = reverse(
                "view_organization", kwargs={"organization_id": self.id}
            )
        if current_organization:
            j["distance"] = self.distance_text(current_organization)
        if include_children:
            j["scopes"] = [s.name for s in self.scopes.all()]
            j["social_media"] = [
                {"id": sm.id, "media_type": sm.media_type, "value": sm.value}
                for sm in self.social_media.all()
            ]
            j["needs"] = [
                n.json(current_organization=current_organization, include_org=False)
                for n in self.needs.all()
            ]
            j["offers"] = [
                o.json(current_organization=current_organization, include_org=False)
                for o in self.offers.all()
            ]

        return j

    def type(self):
        for t in const.ORG_TYPES:
            if t[0] == self.org_type:
                return t[1]
        return ""

    def first_resource_not_set(self, resource_type):
        if resource_type == "needs":
            return self.needs_not_set()[0].code
        return self.offers_not_set()[0].code

    def needs_not_set(self):
        return self.aux_not_set(self.needs.all())

    def offers_not_set(self):
        return self.aux_not_set(self.offers.all())

    def aux_not_set(self, data):
        return self.aux_missing_not_set(list(map(lambda x: x.resource, data)))

    def needs_missing(self):
        return self.aux_missing(self.needs.all())

    def offers_missing(self):
        return self.aux_missing(self.offers.all())

    def aux_missing(self, data):
        return self.aux_missing_not_set(
            list(map(lambda x: x.resource, [x for x in data if x.has_resource]))
        )

    def aux_missing_not_set(self, has):
        return [Resource(x) for x in const.RESOURCES if x[0] not in has]

    def has_scope(self, scope):
        return scope in map(lambda x: x.name, self.scopes.all())

    # haversine formula
    def distance(self, other):
        lat1, lon1 = self.lat, self.lng
        lat2, lon2 = other.lat, other.lng

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        )

        return 2 * 6372.8 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def distance_text(self, other):
        d = self.distance(other)
        if d < 1:
            return _("menys d'un km")
        dc = int(math.ceil(d))
        return _("menys de %(d)skm") % {"d": dc}

    def pending_agreements(self):
        sent = self.sent_agreements.filter(
            communication_accepted=True, agreement_successful=None
        ).count()
        received = self.received_agreements.filter(
            communication_accepted=True, agreement_successful=None
        ).count()
        return sent > 0, received > 0

    def pending_announcement_contacts(self):
        announcements = [a.pending_contacts() for a in self.announcements.all()]
        return len(announcements) > 0 and any(announcements)

    def creator__email(self):
        return self.creator.email


class SocialMedia(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="social_media"
    )
    media_type = models.CharField(max_length=30, choices=const.SOCIAL_MEDIA_TYPES)
    value = models.CharField(max_length=200)


class Resource:
    def __init__(self, values):
        self.code = values[0]
        self.name = values[1]

    def __str__(self):
        return str(self.name)

    @classmethod
    def resource(cls, code):
        for resource in const.RESOURCES:
            if resource[0] == code:
                return Resource(resource)
        raise Exception("Unknown resource")

    @classmethod
    def resource_option(cls, code, option):
        if option == "":
            return ""

        for options in const.RESOURCE_OPTIONS_MAP[code]:
            if options[0] == option:
                return options[1]
        raise Exception("Unknown option")

    def options(self):
        return const.RESOURCE_OPTIONS_MAP[self.code]

    def add_image_label(self):
        return const.RESOURCE_ADD_IMAGE_LABEL[self.code]


class Table:
    def __init__(self, columns, labels, rows):
        self.columns = columns
        self.labels = labels
        self.rows = rows
        self.footer = ["Total"] + [0] * len(rows[0])
        for row in rows:
            for i in range(len(row)):
                self.footer[i + 1] += row[i]

    def plot(self):
        df = pd.DataFrame(
            self.rows,
            columns=self.columns[1:],
            index=map(
                lambda x: x if len(x) < 15 else x[:12].strip() + "...", self.labels
            ),
        )
        return plot_dataframe(df)


class Timeline:
    def __init__(self, rows, name=""):
        self.rows = [0]
        self.index = [timezone.now()]
        self.name = name
        if len(rows) == 0:
            return
        self.index = date_intervals(min(rows), max(rows))[:-1]
        self.rows = self.count(rows, self.index)

    def count(self, dates, date_intervals):
        dates = sorted(dates)
        counts = [0] * len(date_intervals)
        interval_index = 0
        for date in dates:
            while (
                interval_index < len(date_intervals) - 1
                and date > date_intervals[interval_index + 1]
            ):
                interval_index += 1
            counts[interval_index] += 1
        return counts

    def plot(self):
        df = pd.DataFrame(
            self.rows,
            columns=[self.name],
            index=map(lambda x: x.strftime("%Y/%m/%d"), self.index),
        )
        return plot_dataframe(df, figsize=(10, 6))


class Graph:
    def __init__(self, graph, labels):
        self.graph = graph
        self.labels = labels

    def plot(self):
        plt.switch_backend("AGG")
        pos = nx.kamada_kawai_layout(self.graph)
        nx.draw_networkx_labels(self.graph, pos, self.labels)
        nx.draw(self.graph, pos=pos)
        return plot()


def plot_dataframe(df, figsize=(10, 8)):
    plt.switch_backend("AGG")
    df.plot.bar(
        rot=30,
        figsize=figsize,
    )
    return plot()


def plot():
    sio = BytesIO()
    plt.savefig(sio, format="png")
    return base64.encodebytes(sio.getvalue()).decode()


def option_name(code):
    return const.RESOURCE_OPTIONS_DEF_MAP[code]


def resource_name(code):
    return const.RESOURCE_NAMES_MAP[code]


def org_scope_name(code):
    return const.ORG_SCOPES_NAMES_MAP[code]


def org_type_name(code):
    return const.ORG_TYPES_NAMES_MAP[code]


def social_media_type_name(code):
    return const.SOCIAL_MEDIA_TYPES_MAP[code]


def sort_resources(resources):
    return sorted(resources, key=lambda r: const.RESOURCES_ORDER.index(r.resource))


def sort_social_media(social_media):
    return sorted(
        social_media, key=lambda sm: const.SOCIAL_MEDIA_TYPES_ORDER.index(sm.media_type)
    )


class ResourceOption(models.Model):
    name = models.CharField(
        max_length=100, choices=const.RESOURCE_OPTIONS, primary_key=True
    )

    def __str__(self):
        return str(const.RESOURCE_OPTIONS_DEF_MAP[self.name])


class BaseResource(models.Model):
    last_updated_on = models.DateTimeField(auto_now=True)
    resource = models.CharField(max_length=100, choices=const.RESOURCES)
    options = models.ManyToManyField(ResourceOption, blank=True)
    comments = models.TextField(null=True, blank=True)
    has_resource = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(Resource.resource(self.resource))

    def json(self):
        return {
            "id": self.id,
            "resource": self.resource,
            "comments": self.comments,
            "options": [o.name for o in self.options.all()],
        }


class Need(BaseResource):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="needs",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "organization", "resource", name="unique_organization_need"
            ),
        ]

    def json(self, current_organization=None, include_org=True):
        j = super().json()
        j["type"] = "need"
        if include_org:
            j["organization"] = self.organization.json()
        if current_organization:
            j["distance"] = current_organization.distance_text(self.organization)
            j["message_href"] = reverse(
                "send_message",
                args=[
                    current_organization.id,
                    self.organization.id,
                    "need",
                    self.resource,
                ],
            )
        j["images"] = [i.json() for i in self.images.all()]
        return j


class Announcement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="announcements",
    )
    public = models.BooleanField(default=False)
    title = models.TextField(verbose_name=_("Títol"))
    description = models.TextField(verbose_name=_("Descripció"))
    resource = models.CharField(
        max_length=100, choices=const.RESOURCES, verbose_name=_("Recurs")
    )
    option = models.ForeignKey(
        ResourceOption, verbose_name=_("Opció"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "public": self.public,
            "resource": str(self.resource),
            "option": str(self.option),
            "pending_contacts": self.pending_contacts(),
        }

    def pending_contacts(self):
        pc = [c for c in self.contacts.all() if not c.read]
        return len(pc) > 0


class AnnouncementContact(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    received_on = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Contacte enviat el")
    )
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    email = models.EmailField()
    name = models.TextField(verbose_name=_("Nom"))
    message = models.TextField(verbose_name=_("Missatge"))
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-received_on"]

    def json(self):
        return {
            "id": str(self.id),
            "received_on": self.received_on,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "read": self.read,
        }


class Offer(BaseResource):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    charge = models.BooleanField(default=False)
    place_accessible = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "organization", "resource", name="unique_organization_offer"
            ),
        ]

    def json(self, current_organization=None, include_org=True):
        j = super().json()
        j["type"] = "offer"
        if include_org:
            j["organization"] = self.organization.json()
        if current_organization:
            j["distance"] = current_organization.distance_text(self.organization)
            j["message_href"] = reverse(
                "send_message",
                args=[
                    current_organization.id,
                    self.organization.id,
                    "offer",
                    self.resource,
                ],
            )
        j["images"] = [i.json() for i in self.images.all()]
        j["charge"] = self.charge
        j["place_accessible"] = self.place_accessible
        return j


class Agreement(models.Model):
    ORIGIN_CHOICES = [
        ("UNKNOWN", _("Origen desconegut")),
        ("MATCHES", _("Pàgina «Has lligat?»")),
        ("SEARCH", _("Pàgina «Descobreix»")),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    solicitor = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="sent_agreements",
        verbose_name=_("Qui sol·licita"),
        null=True,
    )
    solicitee = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="received_agreements",
        verbose_name=_("A qui li sol·liciten"),
        null=True,
    )
    message = models.TextField(verbose_name=_("Missatge"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Petició enviada el"))
    origin = models.CharField(
        max_length=10,
        choices=ORIGIN_CHOICES,
        verbose_name=_("Origen de la petició"),
        default="UNKNOWN",
    )
    resource = models.CharField(
        max_length=100, choices=const.RESOURCES, verbose_name=_("Recurs")
    )
    resource_type = models.CharField(
        max_length=10,
        choices=[("need", _("Necessitat")), ("offer", _("Oferiment"))],
        verbose_name=_("Tipus de lliga"),
    )
    options = models.ManyToManyField(ResourceOption, verbose_name=_("Opcions"))
    communication_accepted = models.BooleanField(
        null=True, verbose_name=_("Conversa per correu")
    )
    communication_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Correu enviat el")
    )
    agreement_successful = models.BooleanField(
        null=True, verbose_name=_("S'ha realitzat l'intercanvi")
    )
    successful_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Intercanvi registrat el")
    )

    class Meta:
        verbose_name = _("Petició")
        verbose_name_plural = _("Peticions")

    def __str__(self):
        return f"«{self.solicitor}» sol·licita «{resource_name(self.resource)}» a «{self.solicitee}»"

    def solicitor_safe(self):
        if self.solicitor:
            return self.solicitor
        return Organization.deleted_organization()

    def solicitee_safe(self):
        if self.solicitee:
            return self.solicitee
        return Organization.deleted_organization()

    def all_messages_json(self):
        return [
            {
                "message": self.message,
                "sent_on": self.date,
                "sent_by": self.solicitor.id,
                "read": True,
            }
        ] + [
            {
                "id": m.id,
                "message": m.message,
                "sent_on": m.sent_on,
                "sent_by": m.sent_by.id,
                "read": m.read,
            }
            for m in self.messages.all()
        ]

    def json(self, organization_id):
        queryset = self.messages.all()
        last_message_on = None
        if queryset.count() > 0:
            messages = sorted(list(queryset), key=lambda m: m.sent_on)
            last_message_on = list(messages)[-1].sent_on
        return {
            "id": self.id,
            "solicitor": self.solicitor_safe().json(),
            "solicitee": self.solicitee_safe().json(),
            "date": self.date,
            "options": [o.name for o in self.options.all()],
            "resource": self.resource,
            "resource_type": self.resource_type,
            "communication_accepted": self.communication_accepted,
            "communication_date": self.communication_date,
            "agreement_successful": self.agreement_successful,
            "successful_date": self.successful_date,
            # use len, because using .filter() defeats the prefetch_related
            "messages_not_read": len(
                [
                    m
                    for m in self.messages.all()
                    if not m.read and m.sent_by.id != organization_id
                ]
            ),
            "last_message_on": last_message_on,
            "href": reverse(
                "agreement",
                kwargs={"organization_id": organization_id, "agreement_id": self.id},
            ),
        }


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    sent_on = models.DateTimeField(auto_now_add=True, verbose_name=_("Enviat el"))
    sent_by = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="messages_sent",
        verbose_name=_("Enviat per"),
        null=True,
    )
    message = models.TextField(verbose_name=_("Missatge"))
    agreement = models.ForeignKey(
        Agreement, on_delete=models.CASCADE, related_name="messages"
    )
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["sent_on"]


class Contact(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    content = models.TextField()

    class Meta:
        verbose_name = _("Contacte")


class EmailSent(models.Model):
    sent_on = models.DateTimeField(auto_now_add=True)
    sent_to = models.TextField()
    subject = models.TextField()
    body = models.TextField()


class ContactDenyList(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name = _("Contacte bloquejat")
        verbose_name_plural = _("Contactes bloquejats")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = clean_form_email(self.email)
        super(ContactDenyList, self).save(*args, **kwargs)


class NeedImage(models.Model):
    resource = models.ForeignKey(Need, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to=need_images_directory_path, validators=[LimitFileSize(10)]
    )

    def json(self):
        return {"url": self.image.url}


class OfferImage(models.Model):
    resource = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to=offer_images_directory_path, validators=[LimitFileSize(10)]
    )

    def json(self):
        return {"url": self.image.url}
