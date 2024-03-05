from django.contrib import admin

from .models import *

class NeedsInline(admin.StackedInline):
    model = Need
    extra = 0

class OffersInline(admin.StackedInline):
    model = Offer
    extra = 0

class SocialMediaInline(admin.StackedInline):
    model = SocialMedia
    extra = 0

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "creator__email"]
    inlines = [NeedsInline, OffersInline, SocialMediaInline]

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "date_joined", "language", "distance_limit_km"]

class AgreementAdmin(admin.ModelAdmin):
    list_display = [
        "solicitor",
        "resource",
        "solicitee",
        "communication_accepted",
        "communication_date",
        "agreement_successful",
        "successful_date",
    ]

    list_filter = [
        "resource",
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
        ("communication_accepted", "communication_date", "agreement_successful", "successful_date"),
    )

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Contact)
admin.site.register(ContactDenyList)
admin.site.register(Page)
