from django.urls import reverse
from django.utils import timezone
from django.templatetags.static import static

from jinja2 import Environment
from femlliga.models import *
from allauth.socialaccount import providers

import bleach
import femlliga.constants

def format_time(t):
    return timezone.localtime(t).strftime("%d/%m/%Y a les %H:%M")

def path_parent(path):
    return "/".join(path.split("/")[:-2]) + "/"

def provider_login_url(request, provider_id, **kwargs):
    provider = providers.registry.by_id(provider_id)
    query = kwargs
    if 'next' not in query:
       next_ = request.GET.get('next')
       if next_:
           query['next'] = next_
    else:
        if not query['next']:
           del query['next']

    return provider.get_login_url(request, **query)

def clean(s, style=False):
    tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'table', 'thead',
            'tbody', 'th', 'tr', 'td', 'span', 'div', 'br', 'pre', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    if style:
        tags.append('style')
    return bleach.clean(
        s,
        tags = tags,
        attributes = {
        '*': ['class'],
        'a': ['href', 'title'],
        'th': ['colspan'],
        'img': ['alt'],
        'abbr': 'title',
        'acronym': 'title',
    })

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        "len": len,
        "url": reverse,
        "static": static,
        "resource_name": resource_name,
        "org_type_name": org_type_name,
        "org_scope_name": org_scope_name,
        "format_time": format_time,
        "consts": femlliga.constants,
        "enumerate": enumerate,
        "resource_icon": lambda x: femlliga.constants.RESOURCE_ICONS_MAP[x],
        "sort_resources": sort_resources,
        "parent": path_parent,
        "provider_login_url": provider_login_url,
        "clean": clean,
    })
    return env
