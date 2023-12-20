import pytz
import time

from django.conf import settings
from django.utils import timezone, translation
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import redirect_to_login

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate("Europe/Madrid")
        return self.get_response(request)

SESSION_TIMEOUT_KEY = "_session_init_timestamp_"

class LocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "session") or request.session.is_empty():
            return self.get_response(request)

        if request.user and request.user.language:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = translation.get_language()

        return self.get_response(request)

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "session") or request.session.is_empty():
            return self.get_response(request)

        if not request.user.is_staff:
            return self.get_response(request)

        init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())
        expire_seconds = 15 * 60
        session_is_expired = time.time() - init_time > expire_seconds

        if session_is_expired:
            request.session.flush()
            messages.success(request, _("S'ha tancat la sessió per inactivitat"))
            return redirect_to_login(next=request.path, login_url="/admin/login/")

        grace_period = 1
        if time.time() - init_time > grace_period:
            request.session[SESSION_TIMEOUT_KEY] = time.time()

        return self.get_response(request)

