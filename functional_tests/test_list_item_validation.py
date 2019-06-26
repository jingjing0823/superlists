from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        #李小姐访问首页，不小心提交了一个空的代办事项
        #输入框中没有填写任何内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        #首页刷新了，显示一个错误消息
        #错误消息提示代办事项不能为空
        self.wait_for(
         lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        "your can't hava an empty list item"
        )
        )
        
        #李小姐输入了一些文字，再次提交，能正常提交
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        
        #李小姐又提交了一个空的代办事项
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        
        
        #在代办事项清单页面，出现了一个与首页类似的错误消息提示代办事项不能为空
        self.wait_for(
         lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        "your can't hava an empty list item"
        )
        )
        #李小姐输入文字后提交，能正常提交了
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
        self.fail('write me')
 

