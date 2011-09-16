"""Forms used by the data catalog."""

from django import forms
from models import App, Project, Data


class AppForm(forms.ModelForm):
    """Form for users to submit an application."""

    class Meta:
        model = App
        fields = ('name', 'url', 'description', 'tags')


class ProjectForm(forms.ModelForm):
    """Form to submit a project."""

    class Meta:
        model = Project
        fields = ('name', 'organization', 'video_url', 'description',
                  'image', 'tags')


class DataForm(forms.ModelForm):
    """Form for users to submit data."""

    class Meta:
        model = Data
        fields = ('name', 'url', 'description', 'tags')


class SupportForm(forms.Form):
    """A form for supporting a project."""
    project = forms.SlugField(max_length=200)
