import os
from typing import Any

import xlrd as xlrd

# excel_file_list = []
# name_course = []


def grade_info(selected_row, selected_col, mode):
    start_row = selected_row - 1
    start_col = selected_col - 1

    if len(name_course) > 0:
        name_course.clear()


class Excel:
    # 文件夹中excel的列表
    excel_file_list = []

    def __init__(self):

        # 读取所有的文件
        self.find_all_excel()
        # 选择的excel名
        self.__excel_name = None
        # 选择的excel对象
        self.__excel_selected = None
        # 所有的sheet
        self.__sheet_list = []
        # 选择的sheet名
        self.__sheet_name = []
        # 选择的sheet对象
        self.__sheet_selected = None

    def find_all_excel(self):
        """
        将目录下的文件显示到框中
        """
        path = os.getcwd() + "..//excel"
        files = os.listdir(path)
        for file in files:
            self.excel_file_list.append(file)
        return self.excel_file_list

    def __get_sheets(self):
        self.__excel_selected = xlrd.open_workbook(os.getcwd() + r"..//excel/" + self.__excel_name)
        # ['平时成绩', 'Sheet2', '考核成绩']
        self.__sheet_list = self.__excel_selected.sheet_names()

    def row_col_length(self, sheet_name):
        self.__sheet_selected = self.__excel_selected.sheet_by_name(sheet_name)
        row = self.__sheet_selected.nrows
        col = self.__sheet_selected.ncols
        return row, col

    def info(self, row, col):
        pass

    @property
    def excel_name(self):
        return self.__excel_name

    @excel_name.setter
    def excel_name(self, excel_name):
        self.__excel_name = excel_name
        self.__get_sheets()

    @property
    def excel_selected(self):
        return self.__excel_selected

    @property
    def sheet_list(self):
        return self.__sheet_list

    @sheet_list.setter
    def sheet_list(self, sheet_list):
        self.__sheet_list = sheet_list

    @property
    def sheet_selected(self):
        return self.__sheet_selected

    @sheet_selected.setter
    def sheet_selected(self, sheet_selected):
        self.__sheet_selected = sheet_selected
