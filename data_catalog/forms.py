"""Forms used by the data catalog."""

from django import forms
from models import App, Idea, Data, Tag


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


class IdeaForm(forms.ModelForm):
    """Form for users to submit an idea."""

    class Meta:
        model = Idea
        exclude = ('slug',)
