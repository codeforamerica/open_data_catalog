"""Views for the Boston Data Catalog."""

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def home(request):
    """Render the home page."""
    return render_to_response('home.html')


def data(request):
    """Render the data page."""
    return render_to_response('data.html')


def apps(request):
    """Render the apps page."""
    return render_to_response('apps.html')


def ideas(request):
    """Render the ideas page."""
    return render_to_response('ideas.html')


@login_required
def submit_app(request):
    """
    Allow users that are logged in to submit an app built off
    of our data.
    """
    return render_to_response('submit/app.html')


@login_required
def submit_idea(request):
    """
    Allow users that are logged in to submit an idea for the
    data catalog.
    """
    return render_to_response('submit/idea.html')


@login_required
def submit_data(request):
    """
    Allow users that are logged in to submit data that should be
    added to the data catalog.
    """
    return render_to_response('submit/data.html')
