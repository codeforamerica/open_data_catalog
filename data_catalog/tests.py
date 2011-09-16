"""Tests for the data catalog app."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import simplejson as json
from taggit.models import Tag
from mock import patch, Mock

from data_catalog.models import App, Data, Project, Supporter, Link
from data_catalog.context_processors import settings_context
from data_catalog.forms import AppForm, ProjectForm
from data_catalog.search import Search
from data_catalog.utils import JSONResponse


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('foo', 'foo@bar.com', 'bar')

    def test_home_page_is_working(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_data_page_is_working(self):
        response = self.client.get('/data')
        self.assertEquals(response.status_code, 200)

    def test_apps_page_is_working(self):
        response = self.client.get('/apps')
        self.assertEquals(response.status_code, 200)

    def test_projects_page_is_working(self):
        response = self.client.get('/projects')
        self.assertEquals(response.status_code, 200)

    def test_individual_project_page_is_working(self):
        Project.objects.create(name='Test', description='A test cause.',
                             video_url='http://vimeo.com/12345').save()
        response = self.client.get('/project/test')
        self.assertEquals(response.status_code, 200)

    def test_submit_app_page(self):
        self.client.login(username='foo', password='bar')
        response = self.client.get('/submit/app/')
        self.assertEquals(response.status_code, 200)

    def test_submit_project_page(self):
        self.client.login(username='foo', password='bar')
        response = self.client.get('/submit/project/')
        self.assertEquals(response.status_code, 200)

    def test_submit_data_page(self):
        self.client.login(username='foo', password='bar')
        response = self.client.get('/submit/data/')
        self.assertEquals(response.status_code, 200)

    def test_submit_data_page_for_user_not_logged_in(self):
        response = self.client.get('/submit/data/')
        self.assertEquals(response.status_code, 302)

    def test_static_files_are_sent(self):
        response = self.client.get('/robots.txt')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/humans.txt')
        self.assertEquals(response.status_code, 200)

    @patch('data_catalog.views.Search')
    def test_search_works_for_queries(self, model):
        response = self.client.get('/search?q=test')
        self.assertTrue(model.method_calls)
        self.assertEquals(response.status_code, 200)

    @patch('data_catalog.views.Search')
    def test_search_works_without_query(self, model):
        response = self.client.get('/search?q=')
        self.assertFalse(model.method_calls)
        self.assertEquals(response.status_code, 200)

    def test_autocomplete_works_and_returns_JSON(self):
        Tag.objects.create(name='GIS').save()
        response = self.client.get('/autocomplete?q=g')
        data = json.loads(response.content)
        expected_data = {u'tags': ['GIS']}
        self.assertEqual(data, expected_data)

    def test_autocomplete_works_without_query(self):
        response = self.client.get('/autocomplete')
        data = json.loads(response.content)
        expected_data = {'tags': None}
        self.assertEquals(data, expected_data)

    def test_apps_view_is_working_for_found_tag(self):
        Tag.objects.create(name='GIS').save()
        response = self.client.get('/apps?tag=GIS')
        self.assertEquals(response.status_code, 200)

    def test_apps_view_with_no_matching_tags(self):
        response = self.client.get('/apps?tag=GIS')
        self.assertEquals(response.status_code, 200)


class TestContextProcessors(TestCase):

    def test_settings_context_processors(self):
        request = Mock()
        settings = settings_context(request)['settings']
        self.assertEqual(settings['CITY_NAME'], 'Boston')
        self.assertEqual(settings['CATALOG_URL'], 'opendataboston.org')


class TestModels(TestCase):

    def test_creating_a_tag(self):
        Tag.objects.create(name='GIS').save()
        self.assertQuerysetEqual(Tag.objects.all(), ['GIS'], lambda t: t.name)
        gis = Tag.objects.get(name='GIS')
        self.assertEqual(str(gis), 'GIS')

    def test_tag_slugs_are_unique(self):
        Tag.objects.create(name='GIS').save()
        Tag.objects.create(name='GIS').save()
        self.assertQuerysetEqual(Tag.objects.all(), ['gis', 'gis_1'],
                                 lambda t: t.slug)

    def test_an_app_can_have_tags(self):
        app = App.objects.create(name='My App', url='http://myapp.com',
                                 description='This is my test app.')
        app.tags.add('GIS', 'pollution')
        app.save()
        self.assertEquals(str(app), 'My App')
        self.assertQuerysetEqual(app.tags.all(), ['GIS', 'pollution'],
                                 lambda tag: tag.name)

    def test_data_does_not_need_an_url(self):
        test = Tag.objects.create(name='test')
        test.save()
        data = Data.objects.create(name='My Data', description='Test data.')
        data.tags.add(test)
        data.save()
        self.assertEquals(str(data), 'My Data')
        self.assertQuerysetEqual(Data.objects.all(), ['My Data'],
                                 lambda data: data.name)

    def test_that_a_project_can_be_created(self):
        Project.objects.create(name='Test', description='A test cause.',
                             video_url='http://vimeo.com/12345').save()
        self.assertQuerysetEqual(Project.objects.all(), ['Test'],
                                 lambda project: project.name)
        project = Project.objects.get(name='Test')
        self.assertEquals(str(project), 'Test')

    def test_only_one_project_can_be_featured_at_a_time(self):
        Project.objects.create(name='Test 1', description='Featured project',
                               video_url='http://vimeo.com/12345',
                               featured=True).save()
        featured = Project.objects.filter(featured=True)
        self.assertQuerysetEqual(featured, ['Test 1'],
                                 lambda project: project.name)
        Project.objects.create(name='Test 2', description='Another featured',
                               video_url='http://vimeo.com/123456',
                               featured=True).save()
        featured = Project.objects.filter(featured=True)
        self.assertQuerysetEqual(featured, ['Test 2'],
                                 lambda project: project.name)

    def test_a_supporter_does_not_need_links_and_projects(self):
        project = Project.objects.create(name='Test', description='Test cause.',
                                         video_url='http://vimeo.com/12345')
        project.save()
        user = User.objects.create_user('foo', 'foo@bar.com', 'bar')
        supporter = Supporter.objects.create(user=user)
        supporter.projects.add(project)
        supporter.save()
        self.assertQuerysetEqual(Supporter.objects.all(), [user],
                                 lambda supporter: supporter.user)

    def test_removing_a_supporter_from_a_project(self):
        project = Project.objects.create(name='Test', description='Test cause.',
                                         video_url='http://vimeo.com/12345')
        project.save()
        user = User.objects.create_user('foo', 'foo@bar.com', 'bar')
        supporter = Supporter.objects.create(user=user)
        supporter.projects.add(project)
        self.assertQuerysetEqual(project.supporters.all(), ['foo'],
                                 lambda supporter: supporter.user.username)
        project.supporters.remove(supporter)
        self.assertQuerysetEqual(project.supporters.all(), [],
                                 lambda supporter: supporter.user.username)

    def test_add_project_supporter_static_method(self):
        project = Project.objects.create(name='Test', description='Test cause.',
                                         video_url='http://vimeo.com/12345')
        user = User.objects.create_user('foo', 'foo@bar.com', 'bar')
        Supporter.add_project_supporter(project, user)
        self.assertQuerysetEqual(project.supporters.all(), ['foo'],
                                 lambda supporter: supporter.user.username)

    def test_add_project_supporter_with_a_project_slug(self):
        project = Project.objects.create(name='Test', description='Test cause.',
                                         video_url='http://vimeo.com/12345')
        user = User.objects.create_user('foo', 'foo@bar.com', 'bar')
        project_slug = project.slug
        Supporter.add_project_supporter(project_slug, user)
        self.assertQuerysetEqual(project.supporters.all(), ['foo'],
                                 lambda supporter: supporter.user.username)

    def test_remove_project_supporter_static_method(self):
        project = Project.objects.create(name='Test', description='Test cause.',
                                         video_url='http://vimeo.com/12345')
        user = User.objects.create_user('foo', 'foo@bar.com', 'bar')
        Supporter.add_project_supporter(project, user)
        self.assertQuerysetEqual(project.supporters.all(), ['foo'],
                                 lambda supporter: supporter.user.username)
        Supporter.remove_project_supporter(project, user)
        self.assertQuerysetEqual(project.supporters.all(), [],
                                 lambda supporter: supporter.user.username)


class TestForms(TestCase):

    def test_app_form_is_valid_with_tags(self):
        form = AppForm({
            'name': 'test app',
            'description': 'This is a test form.',
            'url': 'http://testapp.com',
            'tags': 'GIS, test'
        })
        self.assertTrue(form.is_valid)
        form.save()
        tags = App.objects.get().tags.all()
        self.assertQuerysetEqual(tags, ['test', 'GIS'], lambda tag: tag.name)

    def test_project_form_is_valid_without_image_and_tags_are_created(self):
        form = ProjectForm({
            'name': 'test project',
            'organization': 'test organization',
            'video_url': 'http://vimeo.com/12345',
            'description': 'This is a test form.',
            'tags': 'test, data, foobar'
        })
        self.assertTrue(form.is_valid)
        self.assertTrue(form.is_multipart)
        form.save()
        tags = Project.objects.get(name='test project').tags.all()
        self.assertQuerysetEqual(tags, ['test', 'foobar', 'data'],
                                 lambda tag: tag.name)


class TestSearch(TestCase):

    def test_tag_search_resources_method(self):
        app = App.objects.create(name='Test', description='Test', url='test.com')
        app.tags.add('GIS')
        app.save()
        results = Search.find_resources('gis')
        self.assertFalse(results['data'])
        self.assertFalse(results['projects'])
        self.assertQuerysetEqual(results['apps'], ['Test'],
                                 lambda app: app.name)

    def test_tag_search_resources_for_nonexisting_tag(self):
        results = Search.find_resources('foo')
        self.assertFalse(results['apps'])
        self.assertFalse(results['data'])
        self.assertFalse(results['projects'])

    def test_tag_search_resources_can_find_app_by_name(self):
        App.objects.create(name='Test data', description='test',
                           url='http://test.com').save()
        results = Search.find_resources('data')
        self.assertQuerysetEqual(results['apps'], ['Test data'],
                                 lambda app: app.name)

    def test_search_by_tag_for_unknown_related_model(self):
        results = Search.by_tag('test_model', 'tag')
        self.assertEquals(results, None)


class TestUtils(TestCase):

    def test_JSON_response_against_model(self):
        app = App.objects.create(name='Test', description='Test.',
                                 url='http://test.com')
        app.save()
        data = {'app': app}
        response = JSONResponse(data)
        content = json.loads(response.content)
        self.assertTrue(isinstance(content, dict))

    def test_JSON_response_fails_when_passed_a_mock_object(self):
        data = Mock()
        self.assertRaises(TypeError, JSONResponse, data)
