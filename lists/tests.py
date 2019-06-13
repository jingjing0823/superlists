from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item
# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)
    #def test_home_page_returns_correct_html(self):
        #request=HttpRequest()
        #response=home_page(request)
        #html=response.content.decode('utf-8')
        #expected_html=render_to_string('home.html')
        #self.assertTrue(html.startswith('<html>'))
        #self.assertIn('<title>To-Do</title>',html)
        #self.assertTrue(html.endswith("</html>"))
        #self.assertEqual(html,expected_html)
    def test_home_page_returns_correct_html1(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
        
    def test_can_save_a_POST_request(self):
        response=self.client.post('/',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')
        #self.assertIn('A new list item',response.content.decode())
        #self.assertTemplateUsed(response,'home.html')
    def test_only_save_item_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)
        
    def test_redirect_after_POST(self):
        response=self.client.post('/',data={'item_text':'A new list item'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/lists/the_only_list_in_the_world/')    
        

        
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item=Item()
        first_item.text='the first (ever) list item'
        first_item.save()
        
        second_item=Item()
        second_item.text='item second'
        second_item.save()
        
        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        
        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        
        self.assertEqual(first_saved_item.text,'the first (ever) list item')
        self.assertEqual(second_saved_item.text,'item second')
class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text="item 1")
        Item.objects.create(text='item 2')
        response=self.client.get('/lists/the_only_list_in_the_world/')
        #self.assertIn('item 1',response.content.decode())
        #self.assertIn('item 2',response.content.decode())
        self.assertContains(response,'item 1')
        self.assertContains(response,'item 2')
    def test_uses_list_template(self):
        response=self.client.get('/lists/the_only_list_in_the_world/')
        self.assertTemplateUsed(response,'list.html')