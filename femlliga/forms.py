import json
import urllib

import django.forms as forms
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
from allauth.account.forms import LoginForm, SignupForm

from .models import CustomUser, Organization, Contact, Resource
from .constants import *

def http_get(url):
    f = urllib.request.urlopen(url)
    res = json.loads(f.read().decode('utf-8'))
    f.close()
    return res

class PreferencesForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ["language", "notifications_frequency", "accept_communications_automatically"]

class OrganizationForm(forms.ModelForm):
    scopes = forms.MultipleChoiceField(
        required = True,
        widget   = forms.CheckboxSelectMultiple,
        choices  = ORG_SCOPES,
    )
    class Meta:
        model = Organization
        fields = ["name", "logo", "description", "org_type", "lat", "lng", "address"]

    def clean(self):
        super().clean()
        if "lat" in self.cleaned_data and "lng" in self.cleaned_data:
            self.cleaned_data.pop("address", None)
        elif "address" in self.cleaned_data and self.cleaned_data["address"]:
            self._errors.pop("lat", None)
            self._errors.pop("lng", None)
            self.cleaned_data["lat"] = 0
            self.cleaned_data["lng"] = 0
            try:
                address = urllib.parse.quote(self.cleaned_data["address"])
                res = http_get(f"https://nominatim.openstreetmap.org/search?format=json&q={address}")
                self.cleaned_data["lat"] = res[0]["lat"]
                self.cleaned_data["lng"] = res[0]["lon"]
            except:
                pass
        else:
            self._errors["address"] = self.error_class([_("Cal indicar la posició o l'adreça")])

        return self.cleaned_data

class ResourceForm(forms.Form):
    resource = forms.ChoiceField(choices=[("", "-----------")] + RESOURCES)
    options = forms.MultipleChoiceField(choices=RESOURCE_OPTIONS, required=False)
    comments = forms.CharField(required = False)
    charge = forms.BooleanField(required = False)

class ImageForm(forms.Form):
    image = forms.ImageField()

class MessageForm(forms.Form):
    message = forms.CharField(min_length=1)
    options = forms.MultipleChoiceField(choices=RESOURCE_OPTIONS, required=False)

    def __init__(self, *args, **kwargs):
        self.resource = kwargs.pop('resource') # must be done first, if not super().__init__(...) fails
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.resource.options.count() == 0:
            return self.cleaned_data

        if len(self.cleaned_data.get("options", [])) == 0:
            self._errors["options"] = self.error_class([_("Cal indicar una opció com a mínim")])
        return self.cleaned_data

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ["email", "content"]

class CaptchaLoginForm(LoginForm):
    captcha = ReCaptchaField()

class CaptchaSignupForm(SignupForm):
    captcha = ReCaptchaField()
