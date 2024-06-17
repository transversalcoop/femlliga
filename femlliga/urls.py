from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    # no login required
    path("", views.index, name="index"),
    path("talk/", views.contact, name="contact"),
    path(
        "public-announcements/", views.public_announcements, name="public_announcements"
    ),
    path(
        "public-announcements/<uuid:pk>/",
        views.public_announcement,
        name="public_announcement",
    ),
    path("maps/", views.maps, name="maps"),
    path("check-matches/", views.check_matches, name="check_matches"),
    path("search-address/", views.search_address, name="search_address"),
    path("page/<slug:name>/", views.page, name="page"),
    # login required
    path("preferences/", views.preferences, name="preferences"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path("app/", views.app, name="app"),
    path("organization/add/", views.add_organization, name="add_organization"),
    path("organization/<uuid:organization_id>/profile/", views.profile, name="profile"),
    path(
        "organization/<uuid:organization_id>/view/",
        views.view_organization,
        name="view_organization",
    ),
    path(
        "organization/<uuid:organization_id>/edit/",
        views.edit_organization,
        name="edit_organization",
    ),
    path(
        "organization/<uuid:organization_id>/delete-logo/",
        views.delete_organization_logo,
        name="delete_organization_logo",
    ),
    path(
        "organization/<uuid:organization_id>/pre-wizard/",
        views.pre_wizard,
        name="pre-wizard",
    ),
    path(
        "organization/<uuid:organization_id>/mid-wizard/",
        views.mid_wizard,
        name="mid-wizard",
    ),
    path(
        "organization/<uuid:organization_id>/reset-wizard/",
        views.reset_wizard,
        name="reset-wizard",
    ),
    path(
        "organization/<uuid:organization_id>/resources-wizard/<str:resource_type>/resource/<str:resource>/",
        views.resources_wizard,
        name="resources-wizard",
    ),
    path(
        "organization/<uuid:organization_id>/resources-wizard/<str:resource_type>/edit/<str:resource>/",
        views.edit_resources_wizard,
        name="force-resources-wizard",
    ),
    path(
        "organization/<uuid:organization_id>/send-message/<uuid:organization_to>/<str:resource_type>/<str:resource>/",
        views.send_message,
        name="send_message",
    ),
    path("organization/<uuid:organization_id>/search/", views.search, name="search"),
    path("organization/<uuid:organization_id>/matches/", views.matches, name="matches"),
    path(
        "organization/<uuid:organization_id>/agreements/",
        views.agreements,
        name="agreements",
    ),
    path(
        "organization/<uuid:organization_id>/agreements/<uuid:agreement_id>/",
        views.agreement,
        name="agreement",
    ),
    path(
        "organization/<uuid:organization_id>/external-contacts/",
        views.external_contacts,
        name="external_contacts",
    ),
    # for debugging style
    #    path(
    #        "organization/<uuid:organization_id>/agreements/<uuid:agreement_id>/email/view/",
    #        views.view_agreement_email,
    #        name="view_agreement_email",
    #    ),
    path(
        "organization/<uuid:organization_id>/agreements/<uuid:agreement_id>/messages/send/",
        views.send_agreement_message,
        name="send_agreement_message",
    ),
    path(
        "organization/<uuid:organization_id>/agreements/<uuid:agreement_id>/messages/<uuid:message_id>/mark-read/",
        views.mark_message_read,
        name="mark_message_read",
    ),
    path(
        "organization/<uuid:organization_id>/agreements/<uuid:agreement_id>/successful/",
        views.agreement_successful,
        name="agreement_successful",
    ),
    path("uploads/<path:path>", views.uploads, name="uploads"),
    # admin required
    path("report/", views.report, name="report"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin/", admin.site.urls),
    # otherwise tested
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
