from django.contrib import admin

from .models import *

class NeedsInline(admin.StackedInline):
    model = Need
    extra = 0

class OffersInline(admin.StackedInline):
    model = Offer
    extra = 0

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [NeedsInline, OffersInline]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Agreement)
admin.site.register(Contact)
admin.site.register(CustomUser)
admin.site.register(Page)
