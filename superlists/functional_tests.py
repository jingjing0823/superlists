from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser=webdriver.FireFox(executable_path = "/Users/lijing/python-project/study/tools/geckodriver")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("To-Do",self.browser.title)
        self.fail('finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
# driver = webdriver.Firefox(executable_path = "/Users/lijing/python-project/study/tools/geckodriver")
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
