"""Tests for the data catalog app."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from mock import Mock, patch

from data_catalog.views import category
from data_catalog.models import Tag, App, Data, Idea
from data_catalog.context_processors import settings_context
from data_catalog.forms import AppForm, DataForm, IdeaForm


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

    @patch('data_catalog.views.App')
    def test_category_page_is_working(self, model):
        response = self.client.get('/apps/GIS/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(model.objects.filter.called)
        model.objects.filter.assert_called_with(tag='GIS')

    @patch('data_catalog.views.render_response')
    def test_category_view_can_handle_missing_models_gracefully(self, render):
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
        self.assertQuerysetEqual(app.tags.all(), ['GIS', 'pollution'],
                                 lambda tag: tag.name)
        self.assertQuerysetEqual(gis.apps.all(), ['My App'],
                                 lambda app: app.name)
        self.assertEquals(str(app), 'My App')

    def test_data_does_not_need_an_url(self):
        test = Tag.objects.create(name='test')
        test.save()
        data = Data.objects.create(name='My Data', description='Test data.')
        data.tags.add(test)
        data.save()
        self.assertQuerysetEqual(Data.objects.all(), ['My Data'],
                                 lambda data: data.name)
        self.assertEquals(str(data), 'My Data')

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


class TestForms(TestCase):

    def test_form_for_submitting_an_app(self):
        form = AppForm({'name': 'Test', 'description': 'My test form.',
                        'url': 'http://test.com', 'input_tags': 'test, form'})


class TestContextProcessor(TestCase):

    def test_settings_context_context_processor(self):
        mock_request = Mock()
        settings = settings_context(mock_request)['settings']
        self.assertEqual(settings['CITY_NAME'], 'Boston')
        self.assertEqual(settings['CATALOG_URL'], 'opendataboston.org')
