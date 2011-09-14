"""Views for the Boston Data Catalog."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag

from data_catalog.models import App, Project, Data
from data_catalog.utils import JSONResponse
from data_catalog.search import Search


def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def apps(request):
    """Render the apps page."""
    context = create_context(request, 'apps')
    return render(request, 'apps.html', context)


def data(request):
    """Render the data page."""
    context = create_context(request, 'data')
    return render(request, 'data.html', context)


def projects(request):
    """Render all the available projects."""
    context = create_context(request, 'projects')
    return render(request, 'projects.html', context)

def community(request):
    """Render the community page."""
    return render(request, 'community.html')


def create_context(request, model_name):
    """
    This function reduces boilerplate by creating a common context dictionary,
    and also determines whether the number of model instances returned can be
    reduced by a tag.
    """
    tag = request.GET.get('tag')
    results = Search.by_tag(model_name, tag)
    path = model_name.rstrip('s')
    return {'results': results, 'path': path}


def individual_resource(request, resource, slug):
    """Render a specific resource."""
    available_resources = {'app': App, 'data': Data, 'project': Project}
    model = available_resources[resource]
    actual_resource = get_object_or_404(model, slug=slug)
    context = {'resource': actual_resource, 'path': resource}
    return render(request, 'individual_resource.html', context)


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
        results = Tag.objects.filter(name__icontains=query).values('name')
        if not results:
            fake_tags = ['abc', 'abcdef', 'abcdefghi', 'def', 'defghi',
                         'defghijkl', 'ghi', 'ghijkl', 'ghijklmno']
            tags = [tag for tag in fake_tags if query in tag]
        else:
            tags = [tag['name'] for tag in results]
        data['tags'] = tags
    return JSONResponse(data)


@login_required
def submit_resource(request, resource):
    """
    Allow users that are logged in to submit a resource built off
    of our data.
    """
    template = 'submit/%s.html' % resource
    return render(request, template)


def send_text_file(request, name):
    """Easiest way to send `robots.txt` and `humans.txt` files."""
    return render(request, 'text_files/%s.txt' % name, content_type='text/plain')
