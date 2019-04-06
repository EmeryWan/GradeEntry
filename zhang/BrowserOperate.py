import time

from zhang.BrowserSingleton import BrowserSingleton
from zhang.Settings import SettingsInfo


class Browser:

    def __init__(self):
        self.browser = BrowserSingleton.instance()
        self.browser.get(SettingsInfo.WEBSITE)
        # logger.info('打开浏览器，打开 {}'.format(WEBSITE))
        time.sleep(3)
        self.__login_input()
        # 需要填充成绩的input列表
        self.__input_elements = []

    def __login_input(self):
        try:
            login_form = self.browser.find_element_by_id('login-action')
        except:
            login_form = None

        if login_form is not None:
            print("login")
            print(SettingsInfo.USER_ID)
            print(SettingsInfo.PASSWORD)
            if SettingsInfo.USER_ID is not None:
                login_form.find_element_by_id('inputUser').send_keys(SettingsInfo.USER_ID)
            if SettingsInfo.PASSWORD is not None:
                login_form.find_element_by_id('inputPassword').send_keys(SettingsInfo.PASSWORD)

    def __find_table(self):
        # 获得table的上一级div
        try:
            parent_div = self.browser.find_element_by_class_name('data-tab')
            table = parent_div.find_element_by_tag_name('table')
            trs = table.find_elements_by_tag_name('tr')
        except:
            trs = None
        return trs

    def __find_input(self):
        trs = self.__find_table()

        if trs is not None:
            # 获得不是hidden的input
            for tr in trs:
                try:
                    inputs_in_tr = tr.find_elements_by_tag_name('input')
                    for ip in inputs_in_tr:
                        if ip.get_attribute('type') == 'text':
                            self.__input_elements.append(ip)
                except:
                    # 第一行没有可输入的input
                    pass
        else:
            print("error !没有找到input")

    def __do_input(self, grade_list):

        # 处理输入数据长度与实际不符 从1开始
        stu_num = len(grade_list)

        if len(self.__input_elements) != 0:
            for index, ip in enumerate(self.__input_elements):
                # 处理第一次可能输入了数据，临时保存过需要更改 index 从0开始
                try:
                    value = ip.get_attribute('value')
                    if value == '':
                        value = None
                except:
                    value = None

                if value is not None:  # 原始有数据 显示取消资格或重新录入新成绩
                    if is_num(str(ip.get_attribute('value'))):
                        ip.clear()
                        if index < stu_num:
                            ip.send_keys(grade_list[index])
                    else:
                        # 中文字 取消资格
                        pass
                else:
                    ip.send_keys(grade_list[index])

    def start_entry_data(self, grade_list):
        # 查找本页面中的input(text)
        self.__find_input()
        # 输入
        self.__do_input(grade_list)

    def click_all_checkbox(self):
        trs = self.__find_table()

        if trs is not None:
            # 找到一行中的checkbox
            for tr in trs:
                try:
                    input_in_tr = tr.find_elements_by_tag_name('input')
                    for ip in input_in_tr:
                        if ip.get_attribute('type') == 'checkbox':
                            ip.click()
                        else:
                            pass
                except:
                    pass
        # logger.info('本页面的checkbox填充完毕')

    def list_browser_window(self):
        # handles = self.browser.current_window_handle
        handles = self.browser.title
        return handles

    def change_control_window(self, num):
        pass


def is_num(num):
    try:
        float(num)
        return True
    except:
        return False
