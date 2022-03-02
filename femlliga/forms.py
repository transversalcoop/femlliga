import django.forms as forms

from django.utils.translation import gettext_lazy as _

from .models import Organization, Contact, Resource
from .constants import *

class OrganizationForm(forms.ModelForm):
    scopes = forms.MultipleChoiceField(
        required = True,
        widget   = forms.CheckboxSelectMultiple,
        choices  = ORG_SCOPES,
    )
    class Meta:
        model = Organization
        fields = ["name", "org_type", "lat", "lng"]

class ResourceForm(forms.Form):
    resource = forms.ChoiceField(choices=[("", "-----------")] + RESOURCES)
    options = forms.MultipleChoiceField(choices=RESOURCE_OPTIONS, required=False)
    has_resource = forms.CharField(max_length=10)
    comments = forms.CharField(required = False)
    charge = forms.BooleanField(required = False)

    def clean(self):
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
        if len(self.cleaned_data.get("options", [])) == 0:
            self._errors["options"] = self.error_class(["Cal indicar una opció com a mínim"])
        return self.cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "content"]
