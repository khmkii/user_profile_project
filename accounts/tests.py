from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from accounts import views


class SignUpInOutTestViews(TestCase):

    def test_sign_up_url(self):
        found = resolve('accounts/sign_up')
        self.assertEqual(found.func, views.sign_up)

    def test_sign_in_url(self):
        found = resolve('accounts/sign_in')
        self.assertEqual(found.func, views.sign_in)

    def test_sign_out_url(self):
        found = resolve('accounts/sign_out')
        self.assertEqual(found.func, views.sign_out)

    def test_sign_in_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.sign_in(request)
        expected_html = render_to_string('accounts/sign_in.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_sign_up_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.sign_up(request)
        expected_html = render_to_string('accounts\sign_up.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_sign_out_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.sign_out(request)
        expected_html = render_to_string('accounts\sign_out.html')
        self.assertEqual(response.content.decode(), expected_html)
