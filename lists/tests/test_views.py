from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item,List
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
    #def test_only_save_item_when_necessary(self):
        #self.client.get('/')
        #self.assertEqual(Item.objects.count(),0)
        
#class ItemModelTest(TestCase):
#    def test_saving_and_retrieving_items(self):
#        first_item=Item()
#        first_item.text='the first (ever) list item'
#        first_item.save()
        
#        second_item=Item()
#        second_item.text='item second'
#        second_item.save()
        
#        saved_items=Item.objects.all()
#        self.assertEqual(saved_items.count(),2)
        
#        first_saved_item=saved_items[0]
#        second_saved_item=saved_items[1]
        
#        self.assertEqual(first_saved_item.text,'the first (ever) list item')
#        self.assertEqual(second_saved_item.text,'item second')
class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        list_1=List.objects.create()
        Item.objects.create(text="item 1",list=list_1)
        Item.objects.create(text='item 2',list=list_1)
        
        list_2=List.objects.create()
        Item.objects.create(text="other items 1",list=list_2)
        Item.objects.create(text='other items 2',list=list_2)
        
        response=self.client.get(f'/lists/{list_1.id}/')
        #self.assertIn('item 1',response.content.decode())
        #self.assertIn('item 2',response.content.decode())
        self.assertContains(response,'item 1')
        self.assertContains(response,'item 2')
        self.assertNotContains(response,'other items 1')
        self.assertNotContains(response,'other items 2')
        
        response=self.client.get(f'/lists/{list_2.id}/')
        self.assertContains(response,'other items 1')
        self.assertContains(response,'other items 2')
        self.assertNotContains(response,'item 1')
        self.assertNotContains(response,'item 2')
    def test_uses_list_template(self):
        list_=List.objects.create()
        response=self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response,'list.html')
    def test_passes_correct_list_to_template(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()
        response=self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],correct_list)
        
        
class NewListTest(TestCase):
    def test_redirect_after_POST(self):
        response=self.client.post('/lists/new',data={'item_text':'A new list item'})
        #self.assertEqual(response.status_code,302)
        #self.assertEqual(response['location'],'/lists/the_only_list_in_the_world/')
        new_list=List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')
                
    def test_can_save_a_POST_request(self):
        response=self.client.post('/lists/new',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')
        #self.assertIn('A new list item',response.content.decode())
        #self.assertTemplateUsed(response,'home.html')
    def test_validation_errors_are_sent_back_to_home_page(self):
        response=self.client.post('/lists/new',data={"text":''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')
        expected_error=escape("your can't hava an empty list item")
#        print(response.content.decode())
        self.assertContains(response,expected_error)
        
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new',data={'item_text':''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)
        
        
class NewItemTest(TestCase):
    def test_can_save_a_POST_rquest_to_an_existing_list(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()
        self.client.post(
        f'/lists/{correct_list.id}/add_item',
        data={'item_text':'a new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'a new item for an existing list')
        self.assertEqual(new_item.list,correct_list)
    def test_redirect_to_list_view(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()
        response=self.client.post(
        f'/lists/{correct_list.id}/add_item',
        data={'item_text':'a new item for an existing list'}
        )
        self.assertRedirects(response,f'/lists/{correct_list.id}/')    