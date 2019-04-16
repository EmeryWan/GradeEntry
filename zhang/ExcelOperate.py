import os

import xlrd as xlrd

from zhang.Log import LoggerSingleton
from zhang.Settings import SettingsInfo


class Excel:
    def __init__(self):
        self.__excel_name = None
        self.__sheet_lists = None
        # sheetName -> {row:, col:}
        self.__sheet_name_and_row_col = {}
        # sheetName -> [][]
        self.__sheet_name_and_info = {}

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

    def set_sheet_name_and_row_col(self, sheet_name, row_col_info):
        self.__sheet_name_and_row_col[sheet_name] = row_col_info

    def get_sheet_row_col(self, sheet_name):
        return self.__sheet_name_and_row_col[sheet_name]

    def set_sheet_name_and_info(self, sheet_name, value):
        self.__sheet_name_and_info[sheet_name] = value

    def get_sheet_info(self, sheet_name):
        return self.__sheet_name_and_info[sheet_name]


class ExcelOperator:
    # 存放excel的地址
    __excel_files_path = SettingsInfo.EXCEL_FILES_PATH
    # 文件夹中excel的列表
    excel_file_list = []

    def __init__(self):
        self.excel_name_and_object = {}

    def get_excel_object_info(self, excel_name):
        try:
            if self.excel_name_and_object[excel_name] is not None:
                return self.excel_name_and_object[excel_name]
            else:
                return None
        except:
            LoggerSingleton.instance().error("ExcelOperator->get_excel_object_info 内部错误")
            return None

    def get_all_excel_name_lists(self):
        try:
            # 先更新地址
            ExcelOperator.__excel_files_path = SettingsInfo.EXCEL_FILES_PATH

            files = os.listdir(ExcelOperator.__excel_files_path)

            if len(self.excel_file_list) != 0:
                self.excel_file_list.clear()

            # 排除不是excel文件  需要排除临时文件  .~20181-4.xlsx
            if len(files) > 0:
                for file in files:
                    if file.endswith('xlsx') or file.endswith('xls'):
                        if not file.startswith('.') and not file.startswith('~') and not file.startswith(
                                '~$') and not file.startswith('^'):
                            self.excel_file_list.append(file)
            LoggerSingleton.instance().info('ExcelOperator->get_all_excel_name_lists-> ' + str(self.excel_file_list))
            return self.excel_file_list
        except:
            LoggerSingleton.instance().error("ExcelOperator->get_all_excel_name_lists 内部错误")
            return None

    def get_all_info(self, open_excel_name):
        try:
            excel_object = Excel()
            excel_object.excel_name = open_excel_name

            try:
                this_excel = xlrd.open_workbook(os.path.join(ExcelOperator.__excel_files_path, open_excel_name))
            except:
                LoggerSingleton.instance().warning("ExcelOperator->get_all_excel_name_lists 文件被占用")
                this_excel = None

            if this_excel is not None:
                # ['平时成绩', 'Sheet2', '考核成绩']
                sheets = this_excel.sheet_names()
                excel_object.sheet_lists = sheets
                LoggerSingleton.instance().info('ExcelOperator->get_all_info-> ' + str(sheets))

                # 循环获得全部sheet中的信息
                for sheet in sheets:
                    this_sheet = this_excel.sheet_by_name(sheet)

                    # 获得行列信息
                    row = int(this_sheet.nrows)
                    col = int(this_sheet.ncols)
                    row_col_info = {
                        'row': row,
                        'col': col
                    }
                    LoggerSingleton.instance().info('ExcelOperator->get_all_info->all: row:' + str(row) + ', col:' + str(col))

                    excel_object.set_sheet_name_and_row_col(sheet, row_col_info)

                    # 获得单元格信息
                    excel_info = []
                    for r in range(row):
                        row_info = []
                        for c in range(col):
                            row_info.append(this_sheet.cell_value(r, c))
                        excel_info.append(row_info)

                    excel_object.set_sheet_name_and_info(sheet, excel_info)

                self.excel_name_and_object[open_excel_name] = excel_object
                return True
            else:
                LoggerSingleton.instance().warning("ExcelOperator->get_all_excel_name_lists 无文件信息")
                return False
        except:
            LoggerSingleton.instance().error("ExcelOperator->get_all_excel_name_lists 内部错误")

    def get_grade_info(self, excel_name_in, sheet_name_in, row_in, col_in):
        try:
            row_in = int(row_in)
            col_in = int(col_in)

            this_excel_object = self.excel_name_and_object.get(excel_name_in)
            this_sheet_info = this_excel_object.get_sheet_info(sheet_name_in)
            total_row_col_map = this_excel_object.get_sheet_row_col(sheet_name_in)
            row_total = int(total_row_col_map['row'])
            col_total = int(total_row_col_map['col'])

            LoggerSingleton.instance().info('ExcelOperator->get_all_info->select: excel_file:' + str(excel_name_in))
            LoggerSingleton.instance().info('ExcelOperator->get_all_info->select: sheet:' + str(sheet_name_in))
            LoggerSingleton.instance().info('ExcelOperator->get_all_info->select: row:' + str(row_in) + ', col:' + str(col_in))

            # 读取信息
            grade = []

            if row_in <= row_total and col_in <= col_total:
                for r in range(row_in, row_total):
                    try:
                        # 注意类型转换问题
                        temp = this_sheet_info[r][col_in]
                    except ValueError:
                        temp = 0
                    except:
                        temp = 0
                    grade.append(temp)
                LoggerSingleton.instance().info('get_grade_info-> ' + str(grade))
                return grade
            else:
                LoggerSingleton.instance().warning("ExcelOperator->get_grade_info 没有信息")
                return []
        except:
            LoggerSingleton.instance().error("ExcelOperator->get_grade_info 内部错误")

