import time

from selenium.webdriver.support.select import Select

from singleton.BrowserSingleton import BrowserSingleton
from util import Tool
from util.LevelSystem import LevelSystemEnum, FIVE_LEVEL_MAP, TWO_LEVEL_MAP, WebPageLevelSystemEnum
from util.Log import LoggerSingleton
from util.Configuration import SettingsInfo, MAIN_TABLE_PARENT_DIV_CLASS, TAG_TABLE, TAG_TR, TAG_INPUT, \
    ATTRIBUTE_TYPE, ATTRIBUTE_TEXT_TYPE, HUNDRED_DOUBLE_INPUT_BOOL, LOGIN_FORM_ID, USER_INPUT_ID, PASSWORD_INPUT_ID, \
    LOG_ERROR_TEMPLATE, TAG_OPTION, CURRENT_PAGE_LEVEL_SELECT_ID, ATTRIBUTE_CHECKBOX_TYPE, TAG_SELECT, \
    ATTRIBUTE_VALUE, LOG_INFO_TEMP


class BrowserController:

    def __init__(self):
        pass

    @classmethod
    def open_website(cls):
        try:
            BrowserSingleton.instance().get(SettingsInfo.WEBSITE)
            time.sleep(0.1)
            cls.__login_input()
        except BaseException:
            BrowserSingleton.instance().get(SettingsInfo.HOMEPAGE)

    @classmethod
    def re_open_browser(cls):
        try:
            BrowserController.close_browser()
            BrowserController.open_website()
            return True
        except BaseException:
            return False

    @classmethod
    def close_browser(cls):
        BrowserSingleton.close_instance()

    @classmethod
    def __login_input(cls):
        try:
            login_form = BrowserSingleton.instance().find_element_by_id(LOGIN_FORM_ID)
        except BaseException:
            login_form = None

        if login_form is not None:
            if SettingsInfo.USER_ID is not None:
                login_form.find_element_by_id(USER_INPUT_ID).send_keys(SettingsInfo.USER_ID)
            if SettingsInfo.PASSWORD is not None:
                login_form.find_element_by_id(PASSWORD_INPUT_ID).send_keys(SettingsInfo.PASSWORD)

    ##############################

    @classmethod
    def start_entry_data(cls, sign, grade_list):
        """ False 不在指定页面 """

        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (Tool.get_current_fun_name(), str(sign), str(grade_list)))

        cls.__switch_control_to_end_window()

        if sign == LevelSystemEnum.HUNDRED.value:
            cls.start_entry_hundred_mark_system(grade_list)

        if sign == LevelSystemEnum.FIVE.value:
            page_bool = cls.__is_level_page(sign)
            if not page_bool:
                return False
            cls.start_entry_five_level_system(grade_list)

        if sign == LevelSystemEnum.TWO.value:
            page_bool = cls.__is_level_page(sign)
            if not page_bool:
                return False
            cls.start_entry_two_level_system(grade_list)

        return True

    @classmethod
    def __is_level_page(cls, level):
        """ 判断是否在 五级制 两级制 页面 """
        try:
            level_option = BrowserSingleton.instance().find_element_by_id(
                CURRENT_PAGE_LEVEL_SELECT_ID).find_elements_by_tag_name(TAG_OPTION)
        except BaseException:
            return False

        # 百分制
        if level == LevelSystemEnum.HUNDRED.value:
            if len(level_option) > 1:
                return True

        # 五级制
        if level == LevelSystemEnum.FIVE.value:
            level_name = level_option[0].text
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(level_name)))
            if level_name == WebPageLevelSystemEnum.FIVE.value:
                return True

        # 两级制
        if level == LevelSystemEnum.TWO.value:
            level_name = level_option[0].text
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(level_name)))
            if level_name == WebPageLevelSystemEnum.TWO.value:
                return True
        return False

    @classmethod
    def __find_table_tr_elements(cls):
        """ 返回table的每一行 """
        try:
            # 获得table的上一级div
            parent_div = BrowserSingleton.instance().find_element_by_class_name(MAIN_TABLE_PARENT_DIV_CLASS)
            # table
            table = parent_div.find_element_by_tag_name(TAG_TABLE)
            # 每一行
            trs = table.find_elements_by_tag_name(TAG_TR)
        except BaseException:
            trs = None
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
        return trs

    @classmethod
    def start_entry_hundred_mark_system(cls, grade_list):
        try:
            # 存储 input(text) 的集合
            text_input_elements_list = []
            # 输入形式 小数、整数
            double_bool = HUNDRED_DOUBLE_INPUT_BOOL

            # 查找本页面中的input(text)
            trs = cls.__find_table_tr_elements()

            if trs is None:
                # 未在指定页面
                LoggerSingleton.instance().error(
                    LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
                return

            # 获得不是type为text的input(注意 在最后核查页面会同时存在 text/checkbox的input 注意定位方式)
            # 从第二行开始 第一行为 头部
            for tr in trs[1:]:
                # 获得一行的input
                inputs_in_tr = tr.find_elements_by_tag_name(TAG_INPUT)
                for ip in inputs_in_tr:
                    # 获得不是 type=hidden 的input
                    if ip.get_attribute(ATTRIBUTE_TYPE) == ATTRIBUTE_TEXT_TYPE:
                        text_input_elements_list.append(ip)

            # 处理输入数据长度与实际不符
            stu_data_len = len(grade_list)
            if stu_data_len == 0:
                return

            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(stu_data_len)))

            # index 从0开始
            for index, ip in enumerate(text_input_elements_list):
                # 数组越界异常
                if index >= stu_data_len:
                    return

                # 读取的数据是字符串
                input_value_str = grade_list[index]
                if not double_bool and Tool.is_num(input_value_str):
                    try:
                        input_value_str = str(int(float(input_value_str)))
                    except BaseException:
                        # 类型装换错误
                        if not Tool.is_num(input_value_str):
                            continue

                try:
                    original_value = ip.get_attribute(ATTRIBUTE_VALUE)
                except BaseException:
                    original_value = None

                # 原始无数据
                if original_value == "" or original_value is None:
                    try:
                        if Tool.is_num(input_value_str):
                            ip.send_keys(input_value_str)
                    except BaseException:
                        LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (Tool.get_current_fun_name(), "传值1问题"))
                else:
                    # 原始有数据 或显示取消资格或重新录入新成绩
                    if Tool.is_num(original_value):
                        try:
                            ip.clear()
                            if Tool.is_num(input_value_str):
                                ip.send_keys(input_value_str)
                        except BaseException:
                            LoggerSingleton.instance().error(
                                LOG_ERROR_TEMPLATE % (Tool.get_current_fun_name(), "传值2问题"))
        except BaseException:
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))

    @classmethod
    def start_entry_five_level_system(cls, grade_list):

        try:
            # 反转 FIVE_LEVEL_MAP
            five_input_map = {v: k for k, v in FIVE_LEVEL_MAP.items()}
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(five_input_map)))

            select_elements_list = []

            # 获取表格每一行
            trs = cls.__find_table_tr_elements()
            if trs is None:
                return

            # 获取所有的 select 一行只有一个 select
            for tr in trs[1:]:
                try:
                    select_tr = tr.find_element_by_tag_name(TAG_SELECT)
                except BaseException:
                    continue
                select_elements_list.append(select_tr)

            stu_data_len = len(grade_list)
            if stu_data_len == 0:
                return

            # 按行遍历
            for index, select in enumerate(select_elements_list):

                if index < stu_data_len:
                    # 获取值
                    input_value_str = grade_list[index]
                    # 新建 select 对象
                    select_object = Select(select)
                    try:
                        # 根据 map 映射选择
                        select_object.select_by_value(five_input_map.get(input_value_str))
                    except BaseException:
                        continue
        except BaseException:
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))

    @classmethod
    def start_entry_two_level_system(cls, grade_list):

        try:
            # 反转map
            two_input_map = {v: k for k, v in TWO_LEVEL_MAP.items()}
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(two_input_map)))

            select_elements_list = []

            # 获取表格每一行
            trs = cls.__find_table_tr_elements()
            if trs is None:
                return

            # 获取所有的 select
            # 一行只有一个 select
            for tr in trs[1:]:
                try:
                    select_tr = tr.find_element_by_tag_name(TAG_SELECT)
                except BaseException:
                    continue
                select_elements_list.append(select_tr)

            stu_data_len = len(grade_list)

            if stu_data_len == 0:
                return

            # 按行遍历
            for index, select in enumerate(select_elements_list):
                if index < stu_data_len:
                    # 获取值
                    input_value_str = grade_list[index]
                    # 新建 select 对象
                    select_object = Select(select)
                    try:
                        # 根据 map 映射选择
                        select_object.select_by_value(two_input_map.get(input_value_str))
                    except BaseException:
                        continue
        except BaseException:
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))

    @classmethod
    def click_all_checkbox(cls):
        try:
            cls.__find_table_tr_elements()

            trs = cls.__find_table_tr_elements()

            if trs is None:
                return False

            for tr in trs[1:]:
                input_in_tr = tr.find_elements_by_tag_name(TAG_INPUT)
                for ip in input_in_tr:
                    try:
                        if ip.get_attribute(ATTRIBUTE_TYPE) == ATTRIBUTE_CHECKBOX_TYPE:
                            # 判断一下是否为click状态
                            ip.click()
                    except BaseException:
                        continue
            return True
        except BaseException:
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
            return False

    @classmethod
    def clean_input(cls):
        """ 只对百分制有效 """
        try:

            cls.__find_table_tr_elements()

            # 获得所有的input
            trs = cls.__find_table_tr_elements()

            if trs is None:
                return False

            # 循环
            for tr in trs[1:]:
                # 获得所有的 input 每一个都是 Input (hidden)
                inputs = tr.find_elements_by_tag_name(TAG_INPUT)
                for ip in inputs[::-1]:
                    if ip.get_attribute(ATTRIBUTE_TYPE) == ATTRIBUTE_TEXT_TYPE:
                        try:
                            ip.clear()
                            continue
                        except BaseException:
                            continue
            return True
        except BaseException:
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
            return False

    @classmethod
    def __switch_control_to_end_window(cls):
        """
            控制最后一个打开的窗口
            注意：
            handles (type: list) 获得的列表的顺序不是在浏览器中摆放的位置
            以页面"完整加载"的顺序存放
         """
        handles = BrowserSingleton.instance().window_handles
        # 只有一个窗口就控制该窗口
        # 有打开过多个窗口 最后关闭剩一个窗口的情况 必须有此项
        if len(handles) == 1:
            BrowserSingleton.instance().switch_to.window(handles[0])
            # 为记录信息到文本中 该项不是 error
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (Tool.get_current_fun_name(), "switch_len==1"))
        # 打开超过一个窗口就控制最后打开的窗口
        if len(handles) > 1:
            BrowserSingleton.instance().switch_to.window(handles[-1])
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (Tool.get_current_fun_name(), "switch_len>1"))
