from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)
    def test_home_page_returns_correct_html(self):
        request=HttpRequest()
        response=home_page(request)
        html=response.content.decode('utf-8')
        expected_html=render_to_string('home.html')
        #self.assertTrue(html.startswith('<html>'))
        #self.assertIn('<title>To-Do</title>',html)
        #self.assertTrue(html.endswith("</html>"))
        self.assertEqual(html,expected_html)
    def test_home_page_returns_correct_html1(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')