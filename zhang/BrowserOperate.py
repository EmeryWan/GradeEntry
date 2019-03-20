import re

from zhang.BrowserSingleton import BrowserSingleton


def is_num(num):
    try:
        float(num)
        return True
    except:
        return False


class Browser:

    def __init__(self):
        self.browser_singleton = BrowserSingleton()
        self.browser = self.browser_singleton.get_browser()
        self.browser.get('http://jwxt.ecjtu.jx.cn')
        # self.browser.get(r'file:///home/emery/%E6%A1%8C%E9%9D%A2/%E5%BC%A0%E8%80%81%E5%B8%88/%E6%8F%90%E4%BA%A4%E5%90%8E/%E6%88%90%E7%BB%A9%E5%BD%95%E5%85%A5%E5%AD%90%E7%B3%BB%E7%BB%9F.html')
        # self.browser.maximize_window()

        self.__input_elements = []

    def __find_input(self):
        # 获得table的上一级div
        parent_div = self.browser.find_element_by_class_name('data-tab')
        # 获得table
        table = parent_div.find_element_by_tag_name('table')

        # 查找每一个tr
        trs = table.find_elements_by_tag_name('tr')

        # 获得不是hidden的input
        for tr in trs:
            try:
                inputs_in_tr = tr.find_elements_by_tag_name('input')
                for ip in inputs_in_tr:
                    if ip.get_attribute('type') == 'text':
                        self.__input_elements.append(ip)
            except:
                pass

    def __do_input(self, grade_list):
        for index, ip in enumerate(self.__input_elements):

            try:
                value = ip.get_attribute('value')
                if value == '':
                    value = None
            except:
                value = None

            if value is not None:
                if is_num(str(ip.get_attribute('value'))):
                    print('su')
                    ip.clear()
                    ip.send_keys(grade_list[index])
                else:
                    pass
                    # 中文字 取消资格
            else:
                ip.send_keys(grade_list[index])

    def start_entry_data(self, grade_list):
        self.__find_input()
        self.__do_input(grade_list)

    def list_browser_window(self):
        pass

    def change_control_window(self):
        pass


if __name__ == '__main__':
    g = []
    for i in range(1, 39):
        g.append(i)

    b = Browser()
    a = input()

    b.start_entry_data(g)
