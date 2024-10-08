import bleach
from allauth.socialaccount.templatetags.socialaccount import provider_login_url
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.html import json_script
from django.utils.translation import get_language_from_request, gettext, ngettext
from jinja2 import Environment
from pandas.io.formats.style import Styler

import femlliga.constants as consts
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


def style_dataframe(df):
    s = Styler(df)
    s.set_properties(**{"text-align": "left"})
    s.set_table_attributes('class="table table-sm"')
    return s


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


def provider_login_url_wrapper(request, provider, **params):
    return provider_login_url({"request": request}, provider, **params)


def option_is_publishable(resource_type, resource_code, option):
    try:
        return (
            resource_type == "needs"
            and option in consts.NEEDS_PUBLISHABLE_OPTIONS_MAP[resource_code]
        )
    except:
        return False


def publishable_option_description(resource_code, option):
    return consts.NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP.get(
        (resource_code, option), ""
    )


def exist_public_announcements():
    return Announcement.objects.filter(public=True).count() > 0


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
            "consts": consts,
            "enumerate": enumerate,
            "resource_icon": lambda x: consts.RESOURCE_ICONS_MAP[x],
            "resource_description": lambda x: consts.RESOURCE_DESCRIPTIONS_MAP[x],
            "sort_resources": sort_resources,
            "sort_social_media": sort_social_media,
            "parent": path_parent,
            "provider_login_url": provider_login_url_wrapper,
            "clean": clean,
            "style_dataframe": style_dataframe,
            "add_http": add_http,
            "settings": settings,
            "json_script": json_script,
            "js_bool": js_bool,
            "media_type_placeholder": media_type_placeholder,
            "get_language": get_language,
            "wizard_url": wizard_url,
            "get_current_site": get_current_site,
            "display_list": display_list,
            "option_is_publishable": option_is_publishable,
            "publishable_option_description": publishable_option_description,
            "exist_public_announcements": exist_public_announcements,
        }
    )
    return env
