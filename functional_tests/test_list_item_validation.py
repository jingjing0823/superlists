from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        #李小姐访问首页，不小心提交了一个空的代办事项
        #输入框中没有填写任何内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        #首页刷新了，显示一个错误消息
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))
    
        #错误消息提示代办事项不能为空
        #self.wait_for(
         #lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        #"your can't hava an empty list item"))
        
        #李小姐输入了一些文字，再次提交，能正常提交
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        
        #李小姐又提交了一个空的代办事项
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))
        
        #在代办事项清单页面，出现了一个与首页类似的错误消息提示代办事项不能为空
        #self.wait_for(
         #lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        #"your can't hava an empty list item"))
        #李小姐输入文字后提交，能正常提交了
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
        
    def test_cannot_add_dumplicate_items(self):
        #李小姐访问首页输入了一个代办事项
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')
        #李小姐不小心输入了重复的代办事项
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        #李小姐看到了一个帮助消息，提示不能重复
        
        self.wait_for(lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,"you've already get this in your list"))
        
 

