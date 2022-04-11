import json
import urllib

import django.forms as forms
from django.utils.translation import gettext_lazy as _

from captcha.fields import ReCaptchaField
from allauth.account.forms import LoginForm, SignupForm

from .models import CustomUser, Organization, Contact, Resource
from .constants import *

def http_get(url):
    f = urllib.request.urlopen(url)
    res = json.loads(f.read().decode('utf-8'))
    f.close()
    return res

class NotificationsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["notifications_frequency"]

class OrganizationForm(forms.ModelForm):
    scopes = forms.MultipleChoiceField(
        required = True,
        widget   = forms.CheckboxSelectMultiple,
        choices  = ORG_SCOPES,
    )
    class Meta:
        model = Organization
        fields = ["name", "description", "org_type", "lat", "lng", "address"]

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
            self._errors["address"] = self.error_class(["Cal indicar la posició o l'adreça"])

        return self.cleaned_data

class ResourceForm(forms.Form):
    resource = forms.ChoiceField(choices=[("", "-----------")] + RESOURCES)
    options = forms.MultipleChoiceField(choices=RESOURCE_OPTIONS, required=False)
    has_resource = forms.CharField(max_length=10)
    comments = forms.CharField(required = False)
    charge = forms.BooleanField(required = False)

    def clean(self):
        super().clean()
        has_resource = self.cleaned_data.get("has_resource", "no") == "yes"
        resource_options = Resource.resource(self.cleaned_data["resource"]).options()
        missing_options = len(resource_options) > 0 and len(self.cleaned_data.get("options", [])) == 0
        missing_comments = not self.cleaned_data["comments"]
        if has_resource and missing_options and missing_comments:
            self._errors["options"] = self.error_class([
                "Cal indicar una opció com a mínim, o indicar en comentaris altres opcions que us interessarien",
            ])
        return self.cleaned_data

class ImageForm(forms.Form):
    image = forms.ImageField()

class MessageForm(forms.Form):
    message = forms.CharField(min_length=1)
    options = forms.MultipleChoiceField(choices=RESOURCE_OPTIONS, required=True)

    def clean(self):
        super().clean()
        if len(self.cleaned_data.get("options", [])) == 0:
            self._errors["options"] = self.error_class(["Cal indicar una opció com a mínim"])
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
