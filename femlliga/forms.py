import json

import django.forms as forms
from allauth.account.forms import LoginForm, SignupForm
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField

import femlliga.constants as const
from femlliga.models import (
    Agreement,
    Contact,
    Announcement,
    AnnouncementContact,
    CustomUser,
    Organization,
)

from femlliga.utils import spain_provinces_choices


class PreferencesForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            "language",
            "distance_limit_km",
            "notifications_frequency",
            "notify_immediate_communications_received",
            "notify_immediate_announcement_communications_received",
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


class AnnouncementForm(forms.ModelForm):
    option = forms.ChoiceField(choices=const.RESOURCE_OPTIONS, required=True)

    class Meta:
        model = Announcement
        fields = [
            "public",
            "title",
            "description",
            "resource",
        ]

    def clean(self):
        super().clean()
        if self.cleaned_data.get("resource") not in const.NEEDS_PUBLISHABLE_OPTIONS_MAP:
            self.add_error(None, _("Aquest tipus de recurs no és publicable"))

        possible_options = const.NEEDS_PUBLISHABLE_OPTIONS_MAP.get(
            self.cleaned_data.get("resource")
        )
        option = self.cleaned_data.get("option")
        if not possible_options or (option and option not in possible_options):
            self.add_error("option", _("Aquesta opció no és publicable"))

        return self.cleaned_data


class ResourceForm(forms.Form):
    resource = forms.ChoiceField(choices=[("", "-----------")] + const.RESOURCES)
    options = forms.MultipleChoiceField(choices=const.RESOURCE_OPTIONS, required=False)
    comments = forms.CharField(required=False)
    charge = forms.BooleanField(required=False)
    place_accessible = forms.BooleanField(required=False)
    published = forms.JSONField(required=False)

    def clean(self):
        super().clean()
        published = self.cleaned_data.get("published")
        not_publishable_errors, empty_errors = [], []
        resource = self.cleaned_data.get("resource")
        if published:
            for key in published:
                if key not in const.NEEDS_PUBLISHABLE_OPTIONS_MAP[resource]:
                    not_publishable_errors.append(key)
                if not published[key]:
                    empty_errors.append(key)

        if len(empty_errors) > 0:
            self.add_error(
                None, _("Totes les necessitats publicades necessiten una descripció")
            )
        if len(not_publishable_errors) > 0:
            self.add_error(None, _("Aquesta opció no és publicable"))

        return self.cleaned_data


class ImageForm(forms.Form):
    image = forms.ImageField()


class MessageForm(forms.Form):
    message = forms.CharField(min_length=1)
    origin = forms.ChoiceField(choices=Agreement.ORIGIN_CHOICES)
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


class AnnouncementContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = AnnouncementContact
        fields = ["name", "email", "message"]


class CaptchaLoginForm(LoginForm):
    captcha = ReCaptchaField()


class CaptchaSignupForm(SignupForm):
    captcha = ReCaptchaField()


def add_empty_choice(choices):
    choices.insert(0, ("", "-----"))
    return choices


class ReportFilterForm(forms.Form):
    province = forms.ChoiceField(
        choices=add_empty_choice(spain_provinces_choices),
        required=False,
        label=_("Província"),
    )
    org_type = forms.ChoiceField(
        choices=add_empty_choice(const.ORG_TYPES),
        required=False,
        label=_("Tipus d'organització"),
    )
    group_by = forms.ChoiceField(
        choices=[
            ("ORG_TYPE", _("Tipus d'organització")),
            ("ORG_SCOPE", _("Àmbit de treball de l'organització")),
            ("RESOURCE", _("Categoria del recurs")),
            ("RESOURCE_OPTION", _("Etiqueta del recurs")),
        ],
        required=False,
        label=_("Agrupa per"),
    )
    hide_zeroes = forms.BooleanField(
        required=False, label=_("Oculta files amb tot zeros")
    )
