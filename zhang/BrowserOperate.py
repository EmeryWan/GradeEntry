import time

from zhang.BrowserSingleton import BrowserSingleton
from zhang.Settings import SettingsInfo


class BrowserOperate:

    def __init__(self):
        self.open_website()

    def open_website(self):
        BrowserSingleton.instance().get(SettingsInfo.WEBSITE)
        time.sleep(0.5)
        self.__login_input()

    def __login_input(self):
        try:
            login_form = BrowserSingleton.instance().find_element_by_id('login-action')
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

    @classmethod
    def start_entry_data(cls, grade_list):

        text_input_elements_list = []
        trs = cls.__find_table()

        # 查找本页面中的input(text)
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
            # return text_input_elements_list
        else:
            print("error !没有找到input")
            # return []

        # 输入
        # 处理输入数据长度与实际不符 从1开始
        stu_num = len(grade_list)

        if len(text_input_elements_list) != 0:
            for index, ip in enumerate(text_input_elements_list):
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
        # logger.info('本页面的checkbox填充完毕')

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

    # def __find_input(self):
    #
    #     text_input_elements_list = []
    #     trs = self.__find_table()
    #
    #     if trs is not None:
    #         # 获得不是hidden的input
    #         for tr in trs:
    #             try:
    #                 inputs_in_tr = tr.find_elements_by_tag_name('input')
    #                 for ip in inputs_in_tr:
    #                     if ip.get_attribute('type') == 'text':
    #                         text_input_elements_list.append(ip)
    #             except:
    #                 pass  # 第一行没有可输入的input
    #         return text_input_elements_list
    #     else:
    #         print("error !没有找到input")
    #         return []
    #
    # def __do_input(self, grade_list):
    #     text_input_elements_list = self.__find_input()
    #
    #     # 处理输入数据长度与实际不符 从1开始
    #     stu_num = len(grade_list)
    #
    #     if len(text_input_elements_list) != 0:
    #         for index, ip in enumerate(text_input_elements_list):
    #             # 处理第一次可能输入了数据，临时保存过需要更改 index 从0开始
    #             try:
    #                 value = ip.get_attribute('value')
    #                 if value == '':
    #                     value = None
    #             except:
    #                 value = None
    #
    #             if value is not None:  # 原始有数据 显示取消资格或重新录入新成绩
    #                 if is_num(str(ip.get_attribute('value'))):
    #                     ip.clear()
    #                     if index < stu_num:
    #                         ip.send_keys(grade_list[index])
    #                 else:
    #                     # 中文字 取消资格
    #                     pass
    #             else:
    #                 ip.send_keys(grade_list[index])


def is_num(num):
    try:
        float(num)
        return True
    except:
        return False
