"""Views for the Boston Data Catalog."""

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from utils import render_response


def home(request):
    """Render the home page."""
    return render_response(request, 'home.html')


def data(request):
    """Render the data page."""
    return render_response(request, 'data.html')


def apps(request):
    """Render the apps page."""
    return render_response(request, 'apps.html')


def ideas(request):
    """Render the ideas page."""
    return render_response(request, 'ideas.html')


@login_required
def submit_app(request):
    """
    Allow users that are logged in to submit an app built off
    of our data.
    """
    return render_response(request, 'submit/app.html')


@login_required
def submit_idea(request):
    """
    Allow users that are logged in to submit an idea for the
    data catalog.
    """
    return render_response(request, 'submit/idea.html')


@login_required
def submit_data(request):
    """
    Allow users that are logged in to submit data that should be
    added to the data catalog.
    """
    return render_response(request, 'submit/data.html')


def send_text_file(request, name):
    """Easiest way to send `robots.txt` and `humans.txt` files."""
    return render_response(request, 'text_files/%s.txt' % name,
                           mimetype='text/plain')
