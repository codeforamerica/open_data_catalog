"""Forms used by the data catalog."""

from django import forms
from models import App, Cause, Data, Tag


class AppForm(forms.ModelForm):
    """Form for users to submit an application."""
    input_tags = forms.CharField(100)

    class Meta:
        model = App
        exclude = ('slug',)


class DataForm(forms.ModelForm):
    """Form for users to submit data."""

    class Meta:
        model = Data
        exclude = ('slug',)


class CauseForm(forms.ModelForm):
    """Form to add a cause."""

    class Meta:
        model = Cause
        fields = ('name', 'organization', 'video_url', 'image', 'description')
