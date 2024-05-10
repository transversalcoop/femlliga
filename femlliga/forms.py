import json

import django.forms as forms
from allauth.account.forms import LoginForm, SignupForm
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField

from . import constants as const
from .models import Contact, CustomUser, Organization


class PreferencesForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            "language",
            "distance_limit_km",
            "notifications_frequency",
            "notify_immediate_communications_received",
            "notify_agreement_communication_pending",
            "notify_matches",
            "notify_new_resources",
        ]


class OrganizationForm(forms.ModelForm):
    scopes = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=const.ORG_SCOPES,
    )

    class Meta:
        model = Organization
        fields = [
            "name",
            "logo",
            "description",
            "org_type",
            "lat",
            "lng",
            "address",
        ]


class ResourceForm(forms.Form):
    resource = forms.ChoiceField(choices=[("", "-----------")] + const.RESOURCES)
    options = forms.MultipleChoiceField(choices=const.RESOURCE_OPTIONS, required=False)
    comments = forms.CharField(required=False)
    charge = forms.BooleanField(required=False)
    place_accessible = forms.BooleanField(required=False)


class ImageForm(forms.Form):
    image = forms.ImageField()


class MessageForm(forms.Form):
    message = forms.CharField(min_length=1)
    options = forms.MultipleChoiceField(choices=const.RESOURCE_OPTIONS, required=False)

    def __init__(self, *args, **kwargs):
        self.resource = kwargs.pop(
            "resource"
        )  # must be done first, if not super().__init__(...) fails
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.resource.options.count() == 0:
            return self.cleaned_data

        if len(self.cleaned_data.get("options", [])) == 0:
            self.add_error("options", _("Cal indicar una opció com a mínim"))

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
