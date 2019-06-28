import os
import xlrd as xlrd

from util import Tool
from util.Log import LoggerSingleton
from util.Configuration import SettingsInfo, LOG_ERROR_TEMPLATE, LOG_INFO_TEMP


# 单个 Excel 的封装
###########
class Excel:
    def __init__(self):
        # Excel 文件名
        self.__excel_name = None

        # Excel sheet 页
        self.__sheet_lists = None

        # sheet页中的行列信息 只是记录了几行几列
        # { sheetName -> {row:, col:} }
        self.__sheet_map_row_col = {}

        # sheet页中 所有单元格信息
        # sheetName -> [][]
        self.__sheet_map_cell = {}

    @property
    def excel_name(self):
        return self.__excel_name

    @excel_name.setter
    def excel_name(self, value):
        self.__excel_name = value

    @property
    def sheet_lists(self):
        return self.__sheet_lists

    @sheet_lists.setter
    def sheet_lists(self, value):
        self.__sheet_lists = value

    @property
    def sheet_map_row_col(self):
        return self.__sheet_map_row_col

    @property
    def sheet_map_cell(self):
        return self.__sheet_map_cell

    def set_row_col_by_sheet(self, sheet_name, row_col_info):
        self.__sheet_map_row_col[sheet_name] = row_col_info

    def get_row_col_by_sheet(self, sheet_name):
        return self.__sheet_map_row_col[sheet_name]

    def set_cell_by_sheet(self, sheet_name, value):
        self.__sheet_map_cell[sheet_name] = value

    def get_cell_by_sheet(self, sheet_name):
        return self.__sheet_map_cell[sheet_name]


# 存放了所有Excel的信息和相应操作
class ExcelController:
    # 文件夹中excel的列表
    excel_name_list = []
    # 存放每个 excel 的信息
    # { excel名 : Excel 对象 }
    excel_name_object_map = {}

    def __init__(self):
        pass

    # 该方法需要外界调用
    @classmethod
    def read_target_dir_info(cls):
        try:
            cls.__get_excel_name_list()
            cls.__get_all_excel_info()
            return True
        except BaseException:
            return False

    @classmethod
    def __get_excel_name_list(cls):
        # 先更新地址
        path = SettingsInfo.EXCEL_FILES_PATH
        files = os.listdir(path)

        # 清空源数据
        if len(cls.excel_name_list) != 0:
            cls.excel_name_list.clear()

        # 添加数据 排除杂项
        if len(files) > 0:
            for file in files:
                # 只读取 excel
                if file.endswith("xlsx") or file.endswith("xls"):
                    # 临时文件
                    sign_1 = not file.startswith(".")
                    sign_2 = not file.startswith("~")
                    sign_3 = not file.startswith("~$")
                    sign_4 = not file.startswith("^")

                    if sign_1 and sign_2 and sign_3 and sign_4:
                        cls.excel_name_list.append(file)

        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(cls.excel_name_list)))

    @classmethod
    def __get_all_excel_info(cls):
        """ 遍历列表 """
        base_path = SettingsInfo.EXCEL_FILES_PATH
        # 清空全局变量
        excel_map = {}

        for this_excel_name in ExcelController.excel_name_list:

            try:
                this_excel_open = xlrd.open_workbook(os.path.join(base_path, this_excel_name))
            except BaseException:
                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), "文件被占用"))
                continue

            if this_excel_open is not None:
                # 创建 Excel 对象
                excel_object = Excel()
                excel_object.excel_name = this_excel_name
                # ["平时成绩", "Sheet2", "考核成绩"] 会获得隐藏sheet
                sheets = this_excel_open.sheet_names()
                excel_object.sheet_lists = sheets

                # 循环获得 sheets 中信息
                for sheet in sheets:
                    this_sheet = this_excel_open.sheet_by_name(sheet)
                    # 获得行列信息
                    row = int(this_sheet.nrows)
                    col = int(this_sheet.ncols)
                    row_col_info = {"row": row, "col": col}
                    excel_object.set_row_col_by_sheet(sheet, row_col_info)

                    # 获得单元格信息
                    excel_info = []
                    for r in range(row):
                        row_info = []
                        for c in range(col):
                            row_info.append(this_sheet.cell_value(r, c))
                        excel_info.append(row_info)
                    excel_object.set_cell_by_sheet(sheet, excel_info)

                excel_map[this_excel_name] = excel_object

        # 添加该excel信息
        cls.excel_name_object_map = excel_map

        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(cls.excel_name_object_map)))

    @classmethod
    def get_excel_list(cls):
        if len(cls.excel_name_list) > 0:
            return cls.excel_name_list
        else:
            return []

    @classmethod
    def get_view_info_by_name(cls, excel_name):
        """
        返回显示到视图的信息
        :param excel_name:
        :return: 行列 sheet 信息
        """
        if cls.excel_name_object_map[excel_name] is not None:
            # map { sheet_name -> {col, row} }
            return cls.excel_name_object_map[excel_name].sheet_map_row_col
        else:
            return None

    @classmethod
    def get_grade_info_by_col(cls, excel_name_in, sheet_name_in, row_in, col_in):
        try:
            row_in = int(row_in)
            col_in = int(col_in)

            # 获得这个Excel的信息
            this_excel_object = cls.excel_name_object_map[excel_name_in]
            # 通过 sheet 获得单元格信息
            this_sheet_cell_info = this_excel_object.get_cell_by_sheet(sheet_name_in)
            # 通过 sheet 获得总行列数
            total_row_col_map = this_excel_object.get_row_col_by_sheet(sheet_name_in)
            row_total = int(total_row_col_map["row"])
            col_total = int(total_row_col_map["col"])

            # 下面可分离 可有两个方法 按行 / 行列
            # 返回的信息 字符串数组 （重构前为int型数组）
            grade = []
            # 读取信息 按列读取
            if row_in <= row_total and col_in <= col_total:
                for r in range(row_in, row_total):
                    try:
                        # 注意类型转换问题
                        temp = str(this_sheet_cell_info[r][col_in])
                    except BaseException:
                        temp = ""
                    grade.append(temp)
                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(grade)))
                return grade
            else:
                return []
        except BaseException:
            LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
