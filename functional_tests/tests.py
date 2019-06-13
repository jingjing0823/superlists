import unittest

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
import time


class aNewVisitorTestq(unittest.TestCase):

    def setUp(self):
        # self.browser=webdriver.Firefox(executable_path = "/Users/lijing/python-project/study/tools/geckodriver")
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_list_table(self,row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")
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
        time.sleep(2)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        
        inputbox=self.browser.find_element_by_id('id_new_item')
        #再输入一个待办事项
        inputbox.send_keys('use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: use peacock feathers to make a fly')
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        #self.assertTrue(
        #any(row.text=='1: Buy peacock feathers' for row in rows
        #),
        #f'New to-do item did not appear in table,content were :\n{table.text}'
        #)
        self.fail('finish the test!')
 

if __name__ == '__main__':
    unittest.main(warnings='ignore')
# driver = webdriveraaa.Firefox(executable_path = "/Users/lijing/python-project/study/tools/geckodriver")
# #打开搜狗首页
# driver.get("http://www.sogou.com")
# #清空搜索框输入默认内容
# driver.find_element_by_id("query").clear()
# #在搜索框输入“光荣之路自动化测试”
# driver.find_element_by_id("query").send_keys(u"光荣之路自动化测试")
# #单击“搜索”按钮
# driver.find_element_by_id("stb").click()
# #等待3秒
# #退出浏览器
# driver.quit()
