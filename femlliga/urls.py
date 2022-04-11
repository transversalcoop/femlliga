from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = [
    # no login required
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('page/<slug:name>/', views.page, name='page'),

    # login required
    path('notifications/', views.notifications, name='notifications'),
    path('app/', views.app, name='app'),
    path('organization/add/', views.add_organization, name='add_organization'),
    path('organization/<uuid:organization_id>/view/', views.view_organization, name='view_organization'),
    path('organization/<uuid:organization_id>/edit/', views.edit_organization, name='edit_organization'),
    path('organization/<uuid:organization_id>/pre-wizard/', views.pre_wizard, name='pre-wizard'),
    path('organization/<uuid:organization_id>/mid-wizard/', views.mid_wizard, name='mid-wizard'),
    path('organization/<uuid:organization_id>/post-wizard/', views.post_wizard, name='post-wizard'),
    path('organization/<uuid:organization_id>/reset-wizard/', views.reset_wizard, name='reset-wizard'),
    path('organization/<uuid:organization_id>/resources-wizard/<str:resource_type>/', views.resources_wizard, name='resources-wizard'),
    path('organization/<uuid:organization_id>/resources-wizard/<str:resource_type>/force/<str:resource>/', views.force_resources_wizard, name='force-resources-wizard'),
    path('organization/<uuid:organization_id>/send-message/<uuid:organization_to>/<str:resource_type>/<str:resource>/', views.send_message, name='send_message'),
    path('organization/<uuid:organization_id>/matches/', views.matches, name='matches'),
    path('organization/<uuid:organization_id>/agreements/sent/', views.agreements_sent, name='agreements_sent'),
    path('organization/<uuid:organization_id>/agreements/received/', views.agreements_received, name='agreements_received'),
    path('organization/<uuid:organization_id>/agreement/<uuid:agreement_id>/connect/', views.agreement_connect, name='agreement_connect'),
    path('organization/<uuid:organization_id>/agreement/<uuid:agreement_id>/successful/', views.agreement_successful, name='agreement_successful'),

    path('uploads/<path:path>/', views.uploads, name='uploads'),

    # admin required
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),

    # otherwise tested
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
