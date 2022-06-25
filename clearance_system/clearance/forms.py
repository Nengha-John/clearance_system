from django import forms
from . models import ClearanceRequests, ControlNumbers


class ClearanceRequestForm(forms.ModelForm):
    class Meta:
        model = ClearanceRequests
        fields = ['student']

class ControlNumberForms(forms.ModelForm):
    class Meta:
        model = ControlNumbers
        fields = ['request']