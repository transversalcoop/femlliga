import bleach
from allauth.socialaccount.adapter import get_adapter
from allauth.utils import get_request_param
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.html import json_script
from django.utils.translation import get_language_from_request, gettext, ngettext
from jinja2 import Environment

import femlliga.constants
from femlliga.models import *
from femlliga.utils import wizard_url


def get_language(request):
    if not request:
        return "ca"
    return get_language_from_request(request)


def add_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url


def format_time(t):
    return timezone.localtime(t).strftime("%d/%m/%Y a les %H:%M")


def path_parent(path):
    return "/".join(path.split("/")[:-2]) + "/"


def display_list(l):
    return ", ".join([str(x) for x in l])


def js_bool(value):
    if value:
        return "true"
    return "false"


def media_type_placeholder(media_type):
    try:
        return SOCIAL_MEDIA_TYPES_PLACEHOLDERS[media_type]
    except:
        return ""


# would be great to use directly allauth.socialaccount.templatetags.socialaccount.provider_login_url, but there is no
# way to use it directly in jinja2: explanation https://stackoverflow.com/questions/45174765/use-djangos-allauth-with-jinja2
# and source code https://github.com/pennersr/django-allauth
def provider_login_url(request, provider_id, **kwargs):
    provider = get_adapter(request).get_provider(request, provider_id)
    query = kwargs
    process = query.get("process", None)
    if "next" not in query:
        next = get_request_param(request, "next")
        if next:
            query["next"] = next
        elif process == "redirect":
            query["next"] = request.get_full_path()
    else:
        if not query["next"]:
            del query["next"]

    return provider.get_login_url(request, **query)


def clean(s, style=False):
    tags = [
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "code",
        "em",
        "i",
        "li",
        "ol",
        "strong",
        "ul",
        "table",
        "thead",
        "tbody",
        "th",
        "tr",
        "td",
        "span",
        "div",
        "br",
        "pre",
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
    ]
    if style:
        tags.append("style")
    return bleach.clean(
        s,
        tags=tags,
        attributes={
            "*": ["class"],
            "a": ["href", "title"],
            "th": ["colspan"],
            "img": ["alt"],
            "abbr": "title",
            "acronym": "title",
        },
    )


def environment(**options):
    env = Environment(extensions=["jinja2.ext.i18n"], **options)
    env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)
    env.globals.update(
        {
            "len": len,
            "str": str,
            "range": range,
            "url": reverse,
            "static": static,
            "resource_name": resource_name,
            "social_media_type_name": social_media_type_name,
            "org_type_name": org_type_name,
            "org_scope_name": org_scope_name,
            "format_time": format_time,
            "consts": femlliga.constants,
            "enumerate": enumerate,
            "resource_icon": lambda x: femlliga.constants.RESOURCE_ICONS_MAP[x],
            "sort_resources": sort_resources,
            "sort_social_media": sort_social_media,
            "parent": path_parent,
            "provider_login_url": provider_login_url,
            "clean": clean,
            "add_http": add_http,
            "settings": settings,
            "json_script": json_script,
            "js_bool": js_bool,
            "media_type_placeholder": media_type_placeholder,
            "get_language": get_language,
            "wizard_url": wizard_url,
            "get_current_site": get_current_site,
            "display_list": display_list,
        }
    )
    return env
