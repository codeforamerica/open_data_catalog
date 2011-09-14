"""Forms used by the data catalog."""

from django import forms
from models import App, Project, Data


class AppForm(forms.ModelForm):
    """Form for users to submit an application."""

    class Meta:
        model = App
        exclude = ('slug',)


class ProjectForm(forms.ModelForm):
    """Form to submit a project."""

    class Meta:
        model = Project
        exclude = ('slug',)


class DataForm(forms.ModelForm):
    """Form for users to submit data."""

    class Meta:
        model = Data
        fields = ('name', 'description', 'url', 'tags')
