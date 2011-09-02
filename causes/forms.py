"""Forms used by the data catalog."""

from django import forms
from causes.models import Cause


class CauseForm(forms.ModelForm):
    """Form to add a cause."""

    class Meta:
        model = Cause
        fields = ('name', 'video_url', 'image', 'description')
