import os

import xlrd as xlrd

from zhang.Settings import SettingsInfo


class Excel:
    def __init__(self):
        self.__excel_name = None
        self.__sheet_lists = None
        # sheetname -> {row:, col:}
        self.__sheet_name_and_row_col = {}
        # sheetname -> [][]
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
        return self.excel_name_and_object[excel_name]

    def get_all_excel_name_lists(self):
        """
        将目录下的文件显示到框中
        """
        try:
            files = os.listdir(ExcelOperator.__excel_files_path)

            if len(self.excel_file_list) != 0:
                self.excel_file_list.clear()

            for file in files:
                # 需要排除临时文件  .~20181-4.xlsx
                if not file.startswith('.') and not file.startswith('~') and not file.startswith(
                        '~$') and not file.startswith('^'):
                    if file.endswith('xlsx') or file.endswith('xls'):
                        self.excel_file_list.append(file)
            return self.excel_file_list
        except:
            print('无目标文件夹')
            return None

    def get_all_info(self, open_excel_name):
        # 初始化全部信息 （清空）

        excel_object = Excel()
        excel_object.excel_name = open_excel_name

        this_excel = xlrd.open_workbook(os.path.join(ExcelOperator.__excel_files_path, open_excel_name))
        # 获得所有sheet
        # ['平时成绩', 'Sheet2', '考核成绩']
        sheets = this_excel.sheet_names()
        excel_object.sheet_lists = sheets

        for sheet in sheets:
            this_sheet = this_excel.sheet_by_name(sheet)

            row = this_sheet.nrows
            col = this_sheet.ncols
            row_col_info = {
                'row': row,
                'col': col
            }
            # excel_object.sheet_name_and_row_col[sheet] = row_col_info
            excel_object.set_sheet_name_and_row_col(sheet, row_col_info)

            info = []
            for r in range(row):
                row_info = []
                for c in range(col):
                    row_info.append(this_sheet.cell_value(r, c))
                info.append(row_info)
            # excel_object.sheet_name_and_info[sheet] = info
            excel_object.set_sheet_name_and_info(sheet, info)

        # 循环获得全部sheet中的信息
        # 获得行列信息
        # 获得单元格信息
        self.excel_name_and_object[open_excel_name] = excel_object

    def get_grade_info(self, excel_name_in, sheet_name_in, row_in, col_in):
        this_excel = self.excel_name_and_object.get(excel_name_in)
        this_sheet_info = this_excel.sheet_name_and_info.get(sheet_name_in)
        print(this_sheet_info)
        row_total = this_excel.sheet_row_col.get('row')
        print(row_total)
        col_total = this_excel.sheet_row_col.get('col')
        print(col_total)
        # 读取信息
        grade = []
        if row_in <= row_total and col_in <= col_total:
            for r in range(int(row_in), int(row_total)):
                try:
                    # 注意类型转换问题
                    temp = this_sheet_info[r][col_in]
                    print(temp)
                except ValueError:
                    temp = 0
                except:
                    temp = 0
                grade.append(temp)
            return grade
        return None

    def get_grade_info_with_name(self, row_in, col_in):
        pass

    # @property
    # def excel_name_and_object(self):
    #     return self.excel_name_and_object
    #
    # @excel_name_and_object.setter
    # def excel_name_and_object(self, value):
    #     self._excel_name_and_object = value

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
    # @property
    # def excel_name(self):
    #     return self.__excel_name
    #
    # @excel_name.setter
    # def excel_name(self, excel_name):
    #     self.__excel_name = excel_name
    #
    # @property
    # def excel_selected(self):
    #     return self.__excel_selected
    #
    # @property
    # def sheet_list(self):
    #     return self.__sheet_list
    #
    # @property
    # def sheet_name(self):
    #     return self.__sheet_name
    #
    # @sheet_name.setter
    # def sheet_name(self, sheet_name):
    #     self.__sheet_name = sheet_name
    #
    # @property
    # def sheet_selected(self):
    #     return self.__sheet_selected


# if __name__ == '__main__':
#     excel = Excel()
#
#     # 获得所有文件
#     excel_list = excel.get_all_excel()
#     # ['20181-4.xlsx']
#     print(excel_list)
#
#     # 获得一个文件的sheet
#     excel.excel_name = '20181-4.xlsx'
#     sheet_list = excel.get_all_sheets()
#     # ['平时成绩', 'Sheet2', '考核成绩']
#     print(sheet_list)
#
#     # 设置sheet信息
#     excel.sheet_name = '考核成绩'
#
#     # 获得一个sheet的行列
#     r, c = excel.row_col_length()
#     print(r, " ", c)

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
