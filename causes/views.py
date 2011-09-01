"""Views for the catalog."""

from django.shortcuts import get_object_or_404

from causes.utils import render_response
from causes.models import Cause


def home(request):
    """Render the home page."""
    return render_response(request, 'home.html')


def causes(request):
    """Render all the available causes."""
    return render_response(request, 'causes.html')


def individual_cause(request, cause):
	"""Render a specific cause."""
	specific_cause = get_object_or_404(Cause, slug=cause)
	context = {'cause': specific_cause}
	return render_response(request, 'individual_cause.html', context)
