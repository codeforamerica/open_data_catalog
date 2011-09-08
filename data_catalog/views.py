"""Views for the Boston Data Catalog."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from data_catalog.models import Tag
from data_catalog.utils import JSONResponse
from data_catalog.search import Search
from causes.models import Cause


def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def apps(request):
    """Render the apps page."""
    return reduce_results(request, 'apps', 'apps.html')


def data(request):
    """Render the data page."""
    return reduce_results(request, 'data', 'data.html')


def causes(request):
    """Render all the available causes."""
    return render(request, 'causes.html')


def individual_cause(request, slug):
    """Render a specific cause."""
    specific_cause = get_object_or_404(Cause, slug=slug)
    context = {'cause': specific_cause}
    return render(request, 'individual_cause.html', context)


def reduce_results(request, related_name, template):
    """
    Given a request, the `relative_name` of a view's specific model for Tag
    objects, and a template name, this function determines whether it can
    reduce the number of model instances returned by a specific tag.
    """
    tag = request.GET.get('tag')
    results = Search.category(related_name, tag)
    return render(request, template, results)


def search(request):
    """Handle search requests."""
    query = request.GET.get('q')
    if not query:
        context = {'results': None}
    else:
        results = Search.find_resources(query)
        context = {'results': results}
    return render(request, 'base.html', context)


def autocomplete(request):
    """
    Handle all autocomplete requests from the data catalog's
    search bar.
    """
    data = {}
    query = request.GET.get('q')
    if not query:
        data['tags'] = None
    else:
        tags = Tag.objects.filter(name__istartswith=query)
        data['tags'] = tags
    return JSONResponse(data)


@login_required
def submit_app(request):
    """
    Allow users that are logged in to submit an app built off
    of our data.
    """
    return render(request, 'submit/app.html')


@login_required
def submit_cause(request):
    """
    Allow users that are logged in to submit an idea for the
    data catalog.
    """
    return render(request, 'submit/cause.html')


@login_required
def submit_data(request):
    """
    Allow users that are logged in to submit data that should be
    added to the data catalog.
    """
    return render(request, 'submit/data.html')


def send_text_file(request, name):
    """Easiest way to send `robots.txt` and `humans.txt` files."""
    return render(request, 'text_files/%s.txt' % name, content_type='text/plain')
