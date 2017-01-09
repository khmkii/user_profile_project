from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from user_profile_project import views


class HomePageTest(TestCase):

    def test_root_url_resolves(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
