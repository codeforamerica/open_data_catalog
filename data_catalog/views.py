"""Views for the Boston Data Catalog."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from data_catalog.models import App, Data, Idea, Tag
from data_catalog.utils import render_response, JSONResponse


def home(request):
    """Render the home page."""
    return render_response(request, 'home.html')


def data(request):
    """Render the data page."""
    results = category(request, 'data')
    return render_response(request, 'data.html', results)


def apps(request):
    """Render the apps page."""
    results = category(request, 'apps')
    return render_response(request, 'apps.html', results)


def ideas(request):
    """Render the ideas page."""
    results = category(request, 'ideas')
    return render_response(request, 'ideas.html', results)


def category(request, related_name):
    """
    Given the model `related_name` attribute of the Tag model (apps, ideas,
    data), this function will check to see if a specific tag is being called.
    If not, all of the available records are returned.
    """
    available_models = {'apps': App, 'data': Data, 'ideas': Idea}
    tag = request.GET.get('tag')
    if related_name not in available_models:
        results = None
    elif tag:
        try:
            tag_model = Tag.objects.get(name=tag)
            results = getattr(tag_model, related_name).all()
        except:
            results = []
    else:
        model = available_models[related_name]
        results = model.objects.all()
    context = {'results': results}
    return context


def search(request):
    """Handle search requests."""
    query = request.GET.get('q')
    if not query:
        context = {'results': None}
    else:
        results = Tag.search_resources(query)
        context = {'results': results}
    return render_response(request, 'base.html', context)


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
