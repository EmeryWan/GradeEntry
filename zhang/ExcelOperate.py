import os

import xlrd as xlrd

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
            return None

    def get_all_excel_name_lists(self):
        try:
            files = os.listdir(ExcelOperator.__excel_files_path)

            if len(self.excel_file_list) != 0:
                self.excel_file_list.clear()

            # 排除不是excel文件  需要排除临时文件  .~20181-4.xlsx
            for file in files:
                if not file.startswith('.') and not file.startswith('~') and not file.startswith(
                        '~$') and not file.startswith('^'):
                    if file.endswith('xlsx') or file.endswith('xls'):
                        self.excel_file_list.append(file)
            return self.excel_file_list
        except:
            return None

    def get_all_info(self, open_excel_name):
        print("get_all_info")
        print(open_excel_name)
        excel_object = Excel()
        excel_object.excel_name = open_excel_name

        try:
            this_excel = xlrd.open_workbook(os.path.join(ExcelOperator.__excel_files_path, open_excel_name))
        except:
            print("文件被占用")
            this_excel = None
        print(this_excel)
        print("333--")
        if this_excel is not None:
            # ['平时成绩', 'Sheet2', '考核成绩']
            sheets = this_excel.sheet_names()
            excel_object.sheet_lists = sheets
            print(sheets)

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
                # print(row_col_info)
                excel_object.set_sheet_name_and_row_col(sheet, row_col_info)

                # 获得单元格信息
                excel_info = []
                for r in range(row):
                    row_info = []
                    for c in range(col):
                        # print('r:', r, ' c:', c)
                        row_info.append(this_sheet.cell_value(r, c))
                    # print(row_info)
                    excel_info.append(row_info)

                excel_object.set_sheet_name_and_info(sheet, excel_info)

            self.excel_name_and_object[open_excel_name] = excel_object
            return True
        else:
            return False

    def get_grade_info(self, excel_name_in, sheet_name_in, row_in, col_in):

        row_in = int(row_in)
        col_in = int(col_in)

        this_excel_object = self.excel_name_and_object.get(excel_name_in)
        this_sheet_info = this_excel_object.get_sheet_info(sheet_name_in)
        total_row_col_map = this_excel_object.get_sheet_row_col(sheet_name_in)
        row_total = int(total_row_col_map['row'])
        col_total = int(total_row_col_map['col'])

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
            print(grade)
            print(len(grade))
            return grade
        else:
            return []

    def get_grade_info_with_name(self, row_in, col_in):
        pass


    # def get_all_sheets(self):
    #     try:
    #         self.__excel_selected = xlrd.open_workbook(
    #             os.path.join(ExcelOperator.__excel_files_path, self.__excel_name))
    #         # ['平时成绩', 'Sheet2', '考核成绩']
    #         self.__sheet_list = self.__excel_selected.sheet_names()
    #         return self.__sheet_list
    #     except:
    #         print('Excel被其他应用占用，无法获取')
    #         return None
    #
    # def row_col_length(self):
    #     if self.__sheet_name is not None:
    #         self.__sheet_selected = self.__excel_selected.sheet_by_name(self.__sheet_name)
    #         # 显示行列数是以1开始，取值时以0开始
    #         row = self.__sheet_selected.nrows
    #         col = self.__sheet_selected.ncols
    #         return row, col
    #     return 0, 0
    #
    # def grade_info(self, row_in, col_in):
    #
    #     row_total = self.__sheet_selected.nrows
    #     col_total = self.__sheet_selected.ncols
    #     grade = []
    #
    #     if row_in <= row_total and col_in <= col_total:
    #         for row in range(int(row_in), int(row_total)):
    #             try:
    #                 temp = int(self.__sheet_selected.col_values(int(col_in))[row])
    #             except ValueError:
    #                 temp = 0
    #             except:
    #                 temp = 0
    #             grade.append(temp)
    #         return grade
    #     return None
    #


if __name__ == '__main__':
    eo = ExcelOperator()
    eo.get_all_info('20181-4.xlsx')
    print(eo.excel_name_and_object)
    t = eo.excel_name_and_object.get('20181-4.xlsx')
    print(t.excel_name)
    print(t.sheet_lists)
    print(t.get_sheet_row_col('平时成绩'))
    print(t.get_sheet_info('平时成绩'))
    info = t.t.get_sheet_info('平时成绩')
    # grade = eo.get_grade_info('20181-4.xlsx', '平时成绩', 6, 2)
    # print(grade)
    # {'20181-4.xlsx': <__main__.Excel object at 0x7fd04c14e780>}
# 20181-4.xlsx
# ['平时成绩', 'Sheet2', '考核成绩']
# {'row': 36, 'col': 27}
