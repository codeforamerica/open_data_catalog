"""Forms used by the data catalog."""

from django import forms
from models import App, Cause, Data


class AppForm(forms.ModelForm):
    """Form for users to submit an application."""

    class Meta:
        model = App
        fields = ('name', 'description', 'url')


class CauseForm(forms.ModelForm):
    """Form to submit a cause."""

    class Meta:
        model = Cause
        fields = ('name', 'organization', 'video_url', 'image', 'description')


class DataForm(forms.ModelForm):
    """Form for users to submit data."""

    class Meta:
        model = Data
        fields = ('name', 'description', 'url')


