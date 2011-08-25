"""Views for the Boston Data Catalog."""

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from data_catalog.models import App, Data, Idea, Tag
from data_catalog.utils import render_response


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


def search(request):
    """Handle search requests."""
    query = request.GET.get('q')
    if not query:
        context = {'results': None}
    else:
        tags = Tag.objects.filter(name=query)
        context = {'results': tags}
    return render_response(request, 'base.html', context)


def autocomplete(request):
    """
    Handle all autocomplete requests from the data catalog's
    search bar.
    """
    return render_response(request, 'base.html')


def category(request, model, tag):
    """
    Given a lowercase model name and tag, search for all models linked to
    the given tag. The model is obtained by looking through a dictionary of
    available models.
    """
    available_models = {'apps': App, 'data': Data, 'ideas': Idea}
    try:
        actual_model = available_models[model]
    except KeyError:
        # The model does not exist.
        context = {'results': None}
    else:
        results = actual_model.objects.filter(tag=tag)
        context = {'results': results}
    return render_response(request, 'category.html', context)


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
