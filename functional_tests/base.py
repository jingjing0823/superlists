from selenium import webdriver
import time
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
MAX_WAIT=10
from selenium.common.exceptions import WebDriverException


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        # self.browser=webdriver.Firefox(executable_path = "/Users/lijing/python-project/study/tools/geckodriver")
        self.browser=webdriver.Firefox()
        staging_server=os.getenv('STAGING_SERVER')
        if staging_server:
            self.live_server_url='http://'+staging_server
    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)
                
    def wait_for(self,fn):
        start_time=time.time()
        while True:
            try:
                return fn()
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)
                
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
                                


 

#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
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

