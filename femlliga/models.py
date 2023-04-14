import math
import uuid
import base64
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from io import BytesIO
from pathlib import Path
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import AbstractUser

from .constants import *
from .utils import date_intervals, clean_form_email

@deconstructible
class LimitFileSize:
    def __init__(self, MB):
        self.MB = MB
        self.limit = MB * 1024 * 1024

    def __call__(self, value):
        if value.size > self.limit:
            raise ValidationError(f"L'arxiu és massa gran, hauria d'ocupar menys de {self.MB} MB.")

    def __eq__(self, other):
        return self.MB == other.MB

class CustomUser(AbstractUser):
    notifications_frequency = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES, default="WEEKLY")
    last_notification_date = models.DateTimeField(auto_now_add=True)

    def get_organization(self):
        organizations = self.organizations.all()
        if len(organizations) > 0:
            return organizations[0]
        return None

class Page(models.Model):
    name = models.SlugField(primary_key = True)
    heading = models.TextField()
    subheading = models.TextField(blank=True)
    content = models.TextField()
    image = models.CharField(max_length=100, blank=True)

class OrganizationScope(models.Model):
    name = models.CharField(max_length=100, choices=ORG_SCOPES, primary_key = True)

    def __str__(self):
        return ORG_SCOPES_NAMES_MAP[self.name]

class Organization(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
    )
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    scopes = models.ManyToManyField(OrganizationScope)
    org_type = models.CharField(max_length=100, choices=ORG_TYPES)
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

    def __str__(self):
        return f"(Entitat) {self.name}"

    def type(self):
        for t in ORG_TYPES:
            if t[0] == self.org_type:
                return t[1]
        return ""

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
        return self.aux_missing_not_set(list(map(lambda x: x.resource, [x for x in data if x.has_resource])))

    def aux_missing_not_set(self, has):
        l = []
        for resource in RESOURCES:
            if resource[0] not in has:
                l.append(Resource(resource))
        return l

    def has_scope(self, scope):
        return scope in map(lambda x: x.name, self.scopes.all())

    # haversine formula
    def distance(self, other):
        lat1, lon1 = self.lat, self.lng
        lat2, lon2 = other.lat, other.lng

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

        return 2*6372.8*math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def distance_text(self, other):
        d = self.distance(other)
        if d < 1:
            return "menys d'un km"
        dc = int(math.ceil(d))
        return f"menys de {dc}km"

    def pending_agreements(self):
        sent = self.sent_agreements.filter(communication_accepted=True, agreement_successful=None)
        received0 = self.received_agreements.filter(communication_accepted=None)
        received1 = self.received_agreements.filter(communication_accepted=True, agreement_successful=None)
        return len(sent) > 0, len(received0) > 0 or len(received1) > 0

class SocialMedia(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="social_media")
    media_type = models.CharField(max_length=30, choices=SOCIAL_MEDIA_TYPES)
    value = models.CharField(max_length=200)

class Resource:
    def __init__(self, values):
        self.code = values[0]
        self.name = values[1]

    def __str__(self):
        return self.name

    @classmethod
    def resource(cls, code):
        for resource in RESOURCES:
            if resource[0] == code:
                return Resource(resource)
        raise Exception("Unknown resource")

    @classmethod
    def resource_option(cls, code, option):
        if option == "":
            return ""

        for options in RESOURCE_OPTIONS_MAP[code]:
            if options[0] == option:
                return options[1]
        raise Exception("Unknown option")

    def question(self, resource_type):
        if resource_type == "offers":
            return RESOURCE_OFFER_DESCRIPTIONS[self.code]
        return RESOURCE_NEED_DESCRIPTIONS[self.code]

    def answer_no(self, resource_type): return self.answer(resource_type, 0)
    def answer_yes(self, resource_type): return self.answer(resource_type, 1)
    def answer(self, resource_type, i):
        if resource_type == "offers":
            return RESOURCE_OFFER_ACTIONS[self.code][i]
        return RESOURCE_NEED_ACTIONS[self.code][i]

    def options(self):
        return RESOURCE_OPTIONS_MAP[self.code]

class Table:
    def __init__(self, columns, labels, rows):
        self.columns = columns
        self.labels = labels
        self.rows = rows
        self.footer = ["Total"] + [0] * len(rows[0])
        for row in rows:
            for i in range(len(row)):
                self.footer[i+1] += row[i]

    def plot(self):
        df = pd.DataFrame(
            self.rows,
            columns = self.columns[1:],
            index = map(lambda x: x if len(x) < 15 else x[:12].strip()+"...", self.labels),
        )
        return plot_dataframe(df)

class Timeline:
    def __init__(self, rows, name = ""):
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
            while interval_index < len(date_intervals)-1 and date > date_intervals[interval_index+1]:
                interval_index += 1
            counts[interval_index] += 1
        return counts

    def plot(self):
        df = pd.DataFrame(
            self.rows,
            columns = [self.name],
            index=map(lambda x: x.strftime("%Y/%m/%d"), self.index),
        )
        return plot_dataframe(df, figsize = (10, 6))

class Graph:
    def __init__(self, graph):
        self.graph = graph

    def plot(self):
        plt.switch_backend("AGG")
        nx.draw_kamada_kawai(self.graph)
        return plot()

def plot_dataframe(df, figsize = (10, 8)):
    plt.switch_backend("AGG")
    df.plot.bar(
        rot = 30,
        figsize = figsize,
    )
    return plot()

def plot():
    sio = BytesIO()
    plt.savefig(sio, format="png")
    return base64.encodebytes(sio.getvalue()).decode()

def option_name(code):    return RESOURCE_OPTIONS_DEF_MAP[code]
def resource_name(code):  return RESOURCE_NAMES_MAP[code]
def org_scope_name(code): return ORG_SCOPES_NAMES_MAP[code]
def org_type_name(code):  return ORG_TYPES_NAMES_MAP[code]
def social_media_type_name(code): return SOCIAL_MEDIA_TYPES_MAP[code]

def sort_resources(resources):
    return sorted(resources, key = lambda r: RESOURCES_ORDER.index(r.resource))

def sort_social_media(social_media):
    return sorted(social_media, key = lambda sm: SOCIAL_MEDIA_TYPES_ORDER.index(sm.media_type))

class ResourceOption(models.Model):
    name = models.CharField(max_length=100, choices=RESOURCE_OPTIONS, primary_key = True)

    def __str__(self):
        return RESOURCE_OPTIONS_DEF_MAP[self.name]

class BaseResource(models.Model):
    resource = models.CharField(max_length=100, choices=RESOURCES)
    options = models.ManyToManyField(ResourceOption)
    comments = models.TextField(null = True, blank = True)
    has_resource = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(Resource.resource(self.resource))

    def get_options(self):
        options = [(x.name, str(x)) for x in self.options.all()]
        return options

class Need(BaseResource):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="needs",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint("organization", "resource", name="unique_organization_need"),
        ]

class Offer(BaseResource):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    charge = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint("organization", "resource", name="unique_organization_offer"),
        ]

class Agreement(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
    )
    solicitor = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name="sent_agreements", null=True)
    solicitee = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name="received_agreements", null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    resource = models.CharField(max_length=100, choices=RESOURCES)
    resource_type = models.CharField(max_length=10, choices=[("need", "need"), ("offer", "offer")])
    options = models.ManyToManyField(ResourceOption)
    communication_accepted = models.BooleanField(null=True)
    communication_date = models.DateTimeField(null=True, blank=True)
    agreement_successful = models.BooleanField(null=True)
    successful_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.id}] {self.solicitor} sol·licita {self.resource} a {self.solicitee}"

    def state(self):
        return f"""{self.resource}. Comunicació: {self.communication_accepted}. Èxit: {self.agreement_successful}."""

    def render_options(self):
        options = [str(x) for x in self.options.all()]
        return ", ".join(options)

class Contact(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    content = models.TextField()

class ContactDenyList(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = clean_form_email(self.email)
        super(ContactDenyList, self).save(*args, **kwargs)

def need_images_directory_path(instance, filename):
    return str(Path("images/needs") / filename)

def offer_images_directory_path(instance, filename):
    return str(Path("images/offers") / filename)

class NeedImage(models.Model):
    resource = models.ForeignKey(Need, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=need_images_directory_path, validators=[LimitFileSize(10)])

class OfferImage(models.Model):
    resource = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=offer_images_directory_path, validators=[LimitFileSize(10)])

