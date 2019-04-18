import time

from GradeEntry.BrowserSingleton import BrowserSingleton
from GradeEntry.Log import LoggerSingleton
from GradeEntry.Settings import SettingsInfo


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
            BrowserSingleton.instance(SettingsInfo.HOMEPAGE)

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
        try:
            # input(text) 的集合
            text_input_elements_list = []

            # 查找本页面中的input(text)
            trs = cls.__find_table()
            if trs is not None:
                # 获得不是type为text的input(注意 在核查页面会同时存在 text/checkbox的input 注意定位方式)
                for tr in trs:
                    try:
                        inputs_in_tr = tr.find_elements_by_tag_name('input')
                        for ip in inputs_in_tr:
                            if ip.get_attribute('type') == 'text':
                                text_input_elements_list.append(ip)
                    except:
                        # 第一行没有可输入的input 直接pass
                        pass
            else:
                LoggerSingleton.instance().warning('BrowserOperate->start_entry_data 未在指定页面')
                # QMessage 请到指定页面
                return False

            # 处理输入数据长度与实际不符
            table_stu_len = len(grade_list)

            try:
                if len(text_input_elements_list) != 0:
                    for index, ip in enumerate(text_input_elements_list):
                        # 处理第一次可能输入了数据，临时保存过需要更改 或显示取消资格等不可输入  index 从0开始
                        try:
                            value = ip.get_attribute('value')
                            if value == '':
                                value = None
                        except:
                            LoggerSingleton.instance().error('BrowserOperate->start_entry_data 读取页面input问题')
                            value = ''

                        # 数组越界异常
                        if index < table_stu_len:
                            input_value = grade_list[index]
                            if is_num(input_value):
                                # excel 读取数字默认为float
                                input_value = str(int(input_value))
                        else:
                            input_value = None

                        if input_value is not None:
                            # 原始有数据 或显示取消资格或重新录入新成绩
                            if value is not None:
                                if is_num(str(ip.get_attribute('value'))):
                                    ip.clear()
                                    if index < table_stu_len:
                                        try:
                                            ip.send_keys(input_value)
                                        except:
                                            LoggerSingleton.instance().error(
                                                'BrowserOperate->start_entry_data 1 send_keys问题')
                                            pass
                                else:
                                    # 上面显示中文字 取消资格等 直接pass
                                    pass
                            else:
                                if index < table_stu_len:
                                    try:
                                        ip.send_keys(input_value)
                                    except:
                                        LoggerSingleton.instance().error(
                                            'BrowserOperate->start_entry_data 2 send_keys问题')
            except:
                LoggerSingleton.instance().error('BrowserOperate->start_entry_data 数据处理与传值问题')
            return True
        except:
            LoggerSingleton.instance().error('BrowserOperate->start_entry_data 内部错误')

    @classmethod
    def click_all_checkbox(cls):
        try:
            trs = cls.__find_table()

            if trs is not None:
                # 找到一行中的checkbox
                for tr in trs:
                    try:
                        input_in_tr = tr.find_elements_by_tag_name('input')
                        for ip in input_in_tr:
                            if ip.get_attribute('type') == 'checkbox':
                                # 判断一下是否为click状态
                                ip.click()
                            else:
                                pass
                    except:
                        LoggerSingleton.instance().error('BrowserOperate->click_all_checkbox 勾选checkbox问题')
                        pass
                return True
            else:
                LoggerSingleton.instance().warning('BrowserOperate->click_all_checkbox 未在指定页面')
                # QMessage 请到指定页面
                return False
        except:
            LoggerSingleton.instance().error('BrowserOperate->click_all_checkbox 内部错误')

    @staticmethod
    def __find_table():
        # 获得table的上一级div
        try:
            parent_div = BrowserSingleton.instance().find_element_by_class_name('data-tab')
            table = parent_div.find_element_by_tag_name('table')
            trs = table.find_elements_by_tag_name('tr')
        except:
            LoggerSingleton.instance().error('BrowserOperate->__find_table 内部错误 不在指定页面可能触发')
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
