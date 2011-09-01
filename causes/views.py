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


def individual_cause(request, slug):
	"""Render a specific cause."""
	specific_cause = get_object_or_404(Cause, slug=slug)
	context = {'cause': specific_cause}
	return render_response(request, 'individual_cause.html', context)


def send_text_file(request, name):
    """Easiest way to send `robots.txt` and `humans.txt` files."""
    return render_response(request, 'text_files/%s.txt' % name,
                           mimetype='text/plain')
