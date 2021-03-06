"""Views for the Boston Data Catalog."""

from urllib2 import urlopen

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import simplejson as json
from taggit.models import Tag

from data_catalog.forms import AppForm, DataForm, ProjectForm, SupportForm
from data_catalog.models import App, Data, Project, Supporter, User
from data_catalog.utils import JSONResponse


def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def apps(request):
    """Render the apps page."""
    context = create_context(request, 'apps')
    return render(request, 'apps.html', context)


@cache_page(60 * 10)
def data(request):
    """Render the data page. Currently caching for ten minutes."""
    ping_datacouch()
    context = create_context(request, 'data')
    return render(request, 'data.html', context)


def ping_datacouch():
    """Ping Data Couch to see if there are any new data sets."""
    user = 'newurbanmechs'
    url = 'http://datacouch.com/api/datasets/' + user
    json_data = urlopen(url).read()
    data_sets = json.loads(json_data)
    rows = data_sets['rows']
    Data.check_exists(rows)


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
    page = request.GET.get('page')
    available_models = {'apps': App, 'data': Data, 'projects': Project}
    model = available_models[model_name]
    resources = model.objects.all()
    paginator = Paginator(resources, 9)
    try:
        resources = paginator.page(page)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
    except:
        resources = paginator.page(1)
    path = model_name.rstrip('s')
    context = {'path': path, 'resources': resources}
    context = add_breadcrumb(model_name, context)
    return context


def community(request):
    """Render the community page."""
    featured = Project.featured_project()
    community = User.objects.all()
    context = {'featured': featured, 'community': community}
    return render(request, 'community.html', context)


def community_member(request, username):
    """Render the profile page of a community member by username."""
    profile = User.objects.get(username=username)
    context = {'profile': profile}
    return render(request, 'profile_page.html', context)


def request_data(request):
    """
    Direct the user in the best way for obtaining a currently
    unavailable dataset.
    """
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if name and email and message:
        send_mail(name, message, email, ['nigel.jacob@cityofboston.gov'])
        return redirect(data)
    return render(request, 'request_data.html')


def individual_resource(request, resource_type, slug):
    """Render a specific resource."""
    available_resources = {'app': App, 'project': Project}
    model = available_resources[resource_type]
    resource = get_object_or_404(model, slug=slug)
    context = {
        'resource': resource,
        'path': resource_type,
        'resource_type': resource_type
    }
    if resource_type == 'project':
        supporters = resource.supporters.all()
        context.update({'supporters': supporters})
    template = 'individual_resource/resource.html'
    context = add_breadcrumb(resource_type, context)
    return render(request, template, context)


def redirect_to_data_couch(request, slug):
    """Redirect to Data Couch so that a user can see an actual data set."""
    resource = Data.objects.get(slug=slug)
    redirect_url = 'http://datacouch.com/edit/#/' + resource.slug
    return redirect(redirect_url)


def edit_resource(request, resource_type, slug=None):
    """
    Edit the data associated with a specific model instance with a
    model form.
    """
    available_resources = {
        'app': (App, AppForm),
        'data': (Data, DataForm),
        'project': (Project, ProjectForm),
    }
    model, model_form = available_resources[resource_type]
    if request.method == 'POST':
        # TODO: Check that the user created the project.
        model_instance = model.objects.get(name=request.POST['name'])
        form = model_form(request.POST, instance=model_instance)
        if form.is_valid():
            form.save()
        return redirect(individual_resource, resource_type=resource_type,
                        slug=model_instance.slug)
    elif not slug:
        # Then the project does not exist.
        return redirect(projects)
    model_instance = model.objects.get(slug=slug)
    form = model_form(instance=model_instance)
    context = {'form': form}
    return render(request, 'edit/project.html', context)


@login_required
def my_projects(request):
    """List the projects the user is involved with."""
    user = request.user
    if not user.is_authenticated():
        return redirect(projects)
    projects = Project.objects.filter(user=user)
    context = {'projects': projects}
    return render(request, 'my_projects.html', context)


def add_breadcrumb(resource_type, context):
    """Add a breadcrumb key/value pair to the context dictionary."""
    if resource_type == 'project' or resource_type == 'app':
        breadcrumb = resource_type + 's'
    else:
        breadcrumb = resource_type
    context.update({'breadcrumb': breadcrumb})
    return context


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
            return redirect(thanks)
    context = {'form': form_class, 'resource': resource}
    template = 'submit/%s.html' % resource
    return render(request, template, context)


def thanks(request):
    """Thank a user for submitting a valid resource."""
    return render(request, 'thanks.html')


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
        if results:
            tags = [tag['name'] for tag in results]
        else:
            tags = []
        data['tags'] = tags
    return JSONResponse(data)


def send_text_file(request, name):
    """Easiest way to send `robots.txt` and `humans.txt` files."""
    return render(request, 'text_files/%s.txt' % name, content_type='text/plain')
