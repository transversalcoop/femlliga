import re

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class NeedsInline(admin.TabularInline):
    model = Need
    extra = 0


class OffersInline(admin.TabularInline):
    model = Offer
    extra = 0


class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "creator__email"]
    inlines = [SocialMediaInline, NeedsInline, OffersInline]
    readonly_fields = ("creator",)
    fields = (
        ("name", "creator", "logo"),
        ("description", "scopes"),
        ("org_type", "resources_set"),
        ("lat", "lng"),
        ("address", "city"),
    )


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "date_joined", "language", "distance_limit_km"]
    list_filter = ("email", "language", "distance_limit_km")


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


class AgreementAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = [
        "solicitor",
        "resource",
        "solicitee",
        "origin",
        "communication_accepted",
        "communication_date",
        "agreement_successful",
        "successful_date",
    ]

    list_filter = [
        "resource",
        "origin",
        "communication_accepted",
        "agreement_successful",
    ]

    # agreements are basically immutable
    readonly_fields = (
        "date",
        "solicitor",
        "solicitee",
        "resource",
        "resource_type",
        "options",
        "message",
        "communication_accepted",
        "communication_date",
        "agreement_successful",
        "successful_date",
    )

    fields = (
        ("date", "solicitor", "solicitee"),
        ("resource", "resource_type", "options"),
        ("message",),
        (
            "communication_accepted",
            "communication_date",
            "agreement_successful",
            "successful_date",
        ),
    )


class ContactAdmin(admin.ModelAdmin):
    list_display = ("date", "email", "content")
    list_filter = ("email",)


class PageAdmin(admin.ModelAdmin):
    list_display = ("name", "heading", "language")
    fields = (
        ("name", "language", "image"),
        ("heading", "subheading", "content"),
    )


class EmailSentAdmin(admin.ModelAdmin):
    list_display = ("sent_on", "sent_to", "subject", "email_body")
    CLEAN_IMG = re.compile("<img.*?>")
    STRIP_PADDING = re.compile("padding:.*?;")

    @admin.display(description="Email body")
    def email_body(self, instance):
        body = re.sub(self.CLEAN_IMG, "", instance.body)
        body = re.sub(self.STRIP_PADDING, "", body)
        return mark_safe(body)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactDenyList)
admin.site.register(Page, PageAdmin)
admin.site.register(EmailSent, EmailSentAdmin)
