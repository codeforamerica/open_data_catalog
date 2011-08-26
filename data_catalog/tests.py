"""Tests for the data catalog app."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import simplejson as json
from mock import Mock, patch

from data_catalog.views import category
from data_catalog.models import Tag, App, Data, Idea
from data_catalog.context_processors import settings_context


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('foo', 'foo@bar.com', 'bar')

    def test_home_page_is_working(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_data_page_is_working(self):
        response = self.client.get('/data/')
        self.assertEquals(response.status_code, 200)

    def test_apps_page_is_working(self):
        response = self.client.get('/apps/')
        self.assertEquals(response.status_code, 200)

    def test_ideas_page_is_working(self):
        response = self.client.get('/ideas/')
        self.assertEquals(response.status_code, 200)

    def test_submit_app_page(self):
        self.client.login(username='foo', password='bar')
        response = self.client.get('/submit/app/')
        self.assertEquals(response.status_code, 200)

    def test_submit_idea_page(self):
        self.client.login(username='foo', password='bar')
        response = self.client.get('/submit/idea/')
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

    @patch('data_catalog.views.Tag')
    def test_search_works_for_queries(self, model):
        response = self.client.get('/search?q=test')
        self.assertTrue(model.method_calls)
        self.assertEquals(response.status_code, 200)

    @patch('data_catalog.views.Tag')
    def test_search_works_without_query(self, model):
        response = self.client.get('/search?q=')
        self.assertFalse(model.method_calls)
        self.assertEquals(response.status_code, 200)

    def test_autocomplete_works_and_returns_JSON(self):
        Tag.objects.create(name='GIS').save()
        response = self.client.get('/autocomplete?q=g')
        data = json.loads(response.content)
        expected_data = {u'tags': [{u'id': u'1', u'name': u'GIS'}]}
        self.assertEqual(data, expected_data)

    def test_autocomplete_works_without_query(self):
        response = self.client.get('/autocomplete')
        expected_json = '{\n  "tags": null\n}'
        self.assertEquals(response.content, expected_json)

    @patch('data_catalog.views.App')
    def test_category_page_is_working(self, model):
        response = self.client.get('/apps/GIS/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(model.objects.filter.called)
        model.objects.filter.assert_called_with(tag='GIS')

    @patch('data_catalog.views.render_response')
    def test_category_view_can_handle_missing_models(self, render):
        request = Mock()
        category(request, 'test', 'tag')
        render.assert_called_with(request, 'category.html', {'results': None})


class TestModels(TestCase):

    def test_creating_a_tag(self):
        Tag.objects.create(name='GIS').save()
        self.assertQuerysetEqual(Tag.objects.all(), ['GIS'], lambda t: t.name)
        gis = Tag.objects.get(name='GIS')
        self.assertEqual(str(gis), 'GIS')

    def test_tag_names_are_unique(self):
        Tag.objects.create(name='GIS').save()
        self.assertRaises(IntegrityError, Tag.objects.create, name='GIS')

    def test_an_app_can_have_tags(self):
        gis = Tag.objects.create(name='GIS')
        gis.save()
        pollution = Tag.objects.create(name='pollution')
        pollution.save()
        app = App.objects.create(name='My App', url='http://myapp.com',
                                 description='This is my test app.')
        app.tags.add(gis, pollution)
        app.save()
        self.assertEquals(str(app), 'My App')
        self.assertQuerysetEqual(app.tags.all(), ['GIS', 'pollution'],
                                 lambda tag: tag.name)
        self.assertQuerysetEqual(gis.apps.all(), ['My App'],
                                 lambda app: app.name)

    def test_tag_search_resources_method(self):
        gis = Tag.objects.create(name='GIS')
        gis.save()
        app = App.objects.create(name='Test', description='Test', url='test.com')
        app.tags.add(gis)
        app.save()
        results = Tag.search_resources('gis')
        self.assertQuerysetEqual(results['apps'], ['Test'],
                                 lambda app: app.name)
        self.assertFalse(results['data'])
        self.assertFalse(results['ideas'])

    def test_tag_search_resources_for_nonexisting_tag(self):
        results = Tag.search_resources('foo')
        self.assertFalse(results['apps'])
        self.assertFalse(results['data'])
        self.assertFalse(results['ideas'])

    def test_tag_search_resources_can_find_app_by_name(self):
        App.objects.create(name='Test data', description='test',
                url='http://test.com').save()
        results = Tag.search_resources('data')
        self.assertQuerysetEqual(results['apps'], ['Test data'],
                                 lambda app: app.name)

    def test_data_does_not_need_an_url(self):
        test = Tag.objects.create(name='test')
        test.save()
        data = Data.objects.create(name='My Data', description='Test data.')
        data.tags.add(test)
        data.save()
        self.assertEquals(str(data), 'My Data')
        self.assertQuerysetEqual(Data.objects.all(), ['My Data'],
                                 lambda data: data.name)

    def test_creating_an_idea(self):
        Idea.objects.create(name='Test', description='A test idea.')
        self.assertQuerysetEqual(Idea.objects.all(), ['Test'],
                                 lambda idea: idea.name)
        idea = Idea.objects.get(name='Test')
        self.assertEquals(str(idea), 'Test')

    def test_an_idea_can_have_a_type(self):
        Idea.objects.create(name='App Idea', type='app',
                            description='An idea for an app.')
        self.assertQuerysetEqual(Idea.objects.all(), ['App Idea'],
                                 lambda idea: idea.name)


class TestContextProcessor(TestCase):

    def test_settings_context_context_processor(self):
        request = Mock()
        settings = settings_context(request)['settings']
        self.assertEqual(settings['CITY_NAME'], 'Boston')
        self.assertEqual(settings['CATALOG_URL'], 'opendataboston.org')
