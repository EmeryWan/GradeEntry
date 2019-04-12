import time

from zhang.BrowserSingleton import BrowserSingleton
from zhang.Settings import SettingsInfo


class BrowserOperate:

    def __init__(self):
        self.open_website()

    @classmethod
    def open_website(cls):
        try:
            BrowserSingleton.instance().get(SettingsInfo.WEBSITE)
            time.sleep(0.2)
            cls.__login_input()
        except:
            BrowserSingleton.instance()

    @staticmethod
    def __login_input():
        try:
            login_form = BrowserSingleton.instance().find_element_by_id('login-action')
        except:
            login_form = None

        if login_form is not None:
            if SettingsInfo.USER_ID is not None:
                login_form.find_element_by_id('inputUser').send_keys(SettingsInfo.USER_ID)
            if SettingsInfo.PASSWORD is not None:
                login_form.find_element_by_id('inputPassword').send_keys(SettingsInfo.PASSWORD)

    @classmethod
    def start_entry_data(cls, grade_list):

        # input(text) 的集合
        text_input_elements_list = []

        # 查找本页面中的input(text)
        trs = cls.__find_table()
        if trs is not None:
            # 获得不是hidden的input
            for tr in trs:
                try:
                    inputs_in_tr = tr.find_elements_by_tag_name('input')
                    for ip in inputs_in_tr:
                        if ip.get_attribute('type') == 'text':
                            text_input_elements_list.append(ip)
                except:
                    pass  # 第一行没有可输入的input
        else:
            print("error !没有找到input")
            return False  # QMessage 请到指定页面

        # 处理输入数据长度与实际不符 从1开始
        table_stu_len = len(grade_list)
        print(table_stu_len)

        if len(text_input_elements_list) != 0:
            for index, ip in enumerate(text_input_elements_list):
                # 处理第一次可能输入了数据，临时保存过需要更改 index 从0开始
                try:
                    value = ip.get_attribute('value')
                    if value == '':
                        value = None
                except:
                    value = None

                input_value = grade_list[index]
                if is_num(input_value):
                    input_value = str(int(input_value))

                if value is not None:  # 原始有数据 显示取消资格或重新录入新成绩
                    if is_num(str(ip.get_attribute('value'))):
                        ip.clear()
                        # --------------------- 大于小于两种情况
                        if index < table_stu_len:
                            try:
                                ip.send_keys(input_value)
                            except:
                                pass
                    else:
                        pass  # 上面显示中文字 取消资格等 忽略
                else:
                    if index < table_stu_len:
                        try:
                            ip.send_keys(input_value)
                        except:
                            pass
        return True

    @classmethod
    def click_all_checkbox(cls):
        trs = cls.__find_table()

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
            return True
        else:
            return False  # QMessage 请到指定页面

    @staticmethod
    def __find_table():
        # 获得table的上一级div
        try:
            parent_div = BrowserSingleton.instance().find_element_by_class_name('data-tab')
            table = parent_div.find_element_by_tag_name('table')
            trs = table.find_elements_by_tag_name('tr')
        except:
            trs = None
        return trs

    @staticmethod
    def close_browser():
        BrowserSingleton.close_instance()


def is_num(num):
    try:
        float(num)
        return True
    except:
        return False
