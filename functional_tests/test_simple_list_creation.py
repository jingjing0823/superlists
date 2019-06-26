from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        #self.browser.get("http://localhost:8000")
        self.browser.get(self.live_server_url)
        self.assertIn("To-Do",self.browser.title)
        
        header_text=self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do",header_text)
        #输入代办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
        inputbox.get_attribute('placeholder'),
        "Enter a to-do item"
        )
        #输入一个待办事项
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        
        #再输入一个待办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #验证两个待办事项都在表单中
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: use peacock feathers to make a fly')
        #table=self.browser.find_element_by_id('id_list_table')
        #rows=table.find_elements_by_tag_name('tr')
        #self.assertTrue(
        #any(row.text=='1: Buy peacock feathers' for row in rows
        #),
        #f'New to-do item did not appear in table,content were :\n{table.text}'
        #)
        #self.fail('finish the test!')
    def test_multiple_user_can_start_lists_at_different_urls(self):
        #李小姐打开浏览器
        self.browser.get(self.live_server_url)
        input_box=self.browser.find_element_by_id('id_new_item')
        #李小姐输入代办事项并保存
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #李小姐的清单有一个唯一的url
        miss_li_list_url=self.browser.current_url
        self.assertRegex(miss_li_list_url,'/lists/.+')
        
        #张先生访问了网站
        self.browser.quit()
        self.browser=webdriver.Firefox()
        #张先生访问首页，首页中没有李小姐的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        #张先生输入自己的代办事项
        input_box=self.browser.find_element_by_id('id_new_item')
        input_box.send_keys("buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy milk')
        
        #张先生的清单有一个唯一的url
        mr_zhang_list_url=self.browser.current_url
        self.assertRegex(mr_zhang_list_url,'/lists/.+')
        self.assertNotEqual(miss_li_list_url,mr_zhang_list_url)
        
        #张先生的清单中没有李小姐的代办事项，有自己的代办事项
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('buy milk',page_text)
