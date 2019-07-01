from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):        
    def test_layout_and_styling(self):
        #王小姐访问网站的首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        #王小姐发现输入框居中显示
        input_box=self.get_item_input_box()
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width']/2,512,delta=10)
        
        #王小姐输入一个代办事项并提交，提交后看到输入框也居中显示
        input_box.send_keys("test")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: test')
        
        input_box=self.get_item_input_box()
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width']/2,512,delta=10)
