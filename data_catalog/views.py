"""Views for the Boston Data Catalog."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag

from data_catalog.forms import AppForm, DataForm, ProjectForm, SupportForm
from data_catalog.models import App, Data, Project, Supporter, User
from data_catalog.utils import JSONResponse
from data_catalog.search import Search


def home(request):
    """Render the home page."""
    recent_apps = App.objects.order_by('-id')[:3]
    recent_data = Data.objects.order_by('-id')[:3]
    recent_projects = Project.objects.order_by('-id')[:3]
    featured = featured_project()
    context = {
        'recent_apps': recent_apps,
        'recent_data': recent_data,
        'recent_projects': recent_projects,
        'featured': featured,
    }
    return render(request, 'home.html', context)


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


def community(request):
    """Render the community page."""
    featured = featured_project()
    context = {'featured': featured}
    return render(request, 'community.html', context)


def community_member(request, username):
    """Render the profile page of a community member by username."""
    profile = User.objects.get(username=username)
    context = {'profile': profile}
    return render(request, 'profile_page.html', context)


def featured_project():
    """Return the featured project."""
    try:
        featured = Project.objects.get(featured=True)
    except:
        featured = []
    return featured


def request_data(request):
    """
    Direct the user in the best way for obtaining a currently
    unavailable dataset.
    """
    return render(request, 'request_data.html')


def individual_resource(request, resource_type, slug):
    """Render a specific resource."""
    available_resources = {'app': App, 'data': Data, 'project': Project}
    model = available_resources[resource_type]
    resource = get_object_or_404(model, slug=slug)
    context = {'resource': resource, 'path': resource_type}
    if resource_type == 'project':
        supporters = resource.supporters.all()
        context.update({'supporters': supporters})
        template = 'individual_resource/project.html'
    else:
        template = 'individual_resource/generic.html'
    return render(request, template, context)


@login_required
def submit_resource(request, resource):
    """
    Allow users that are logged in to submit a resource built off
    of our data.
    """
    forms = {'app': AppForm, 'data': DataForm, 'project': ProjectForm}
    form_class = forms[resource]
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return thanks(request, resource)
    context = {'form': form_class}
    template = 'submit/%s.html' % resource
    return render(request, template, context)


def thanks(request, resource):
    """Thank a user for submitting a valid resource."""
    context = {'resource': resource}
    return render(request, 'thanks.html', context)


def support(request):
    """General information on supporting a project."""
    return render(request, 'support/info.html')


def support_project(request, project_slug):
    """Allow a user to support a project."""
    user = request.user
    if not user.is_authenticated():
        url = '/login/?next=project/%s' % (project_slug)
        return redirect(url)
    elif request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            project = get_object_or_404(Project, slug=project_slug)
            Supporter.add_project_supporter(project, user)
            if request.is_ajax():
                success = {'success': True}
                return JSONResponse(success)
            else:
                url = '/project/%s' % (project_slug)
                return redirect(url)
    return redirect(support)


def search(request):
    """Handle search requests."""
    query = request.GET.get('q')
    if not query:
        context = {'results': None}
    else:
        results = Search.find_resources(query)
        context = {'results': results}
    return render(request, 'search.html', context)


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


def send_text_file(request, name):
    """Easiest way to send `robots.txt` and `humans.txt` files."""
    return render(request, 'text_files/%s.txt' % name, content_type='text/plain')
