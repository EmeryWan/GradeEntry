import os

import xlrd as xlrd

from zhang.Settings import SettingsInfo


class Excel:
    # 存放excel的地址
    __excel_files_path = SettingsInfo.EXCEL_FILES_PATH
    # 文件夹中excel的列表
    excel_file_list = []

    def __init__(self):
        # 选择的excel名
        self.__excel_name = None
        # 选择的excel对象
        self.__excel_selected = None
        # 所有的sheet
        self.__sheet_list = []
        # 选择的sheet名
        self.__sheet_name = None
        # 选择的sheet对象 sheet_by_name(sheet_names[sheet_name])
        self.__sheet_selected = None

    def get_all_excel(self):
        """
        将目录下的文件显示到框中
        """
        try:
            files = os.listdir(Excel.__excel_files_path)

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

    def get_all_sheets(self):
        try:
            self.__excel_selected = xlrd.open_workbook(os.path.join(Excel.__excel_files_path, self.__excel_name))
            # ['平时成绩', 'Sheet2', '考核成绩']
            self.__sheet_list = self.__excel_selected.sheet_names()
            return self.__sheet_list
        except:
            print('Excel被其他应用占用，无法获取')
            return None

    def row_col_length(self):
        if self.__sheet_name is not None:
            self.__sheet_selected = self.__excel_selected.sheet_by_name(self.__sheet_name)
            # 显示行列数是以1开始，取值时以0开始
            row = self.__sheet_selected.nrows
            col = self.__sheet_selected.ncols
            return row, col
        return 0, 0

    def grade_info(self, row_in, col_in):

        row_total = self.__sheet_selected.nrows
        col_total = self.__sheet_selected.ncols
        grade = []

        if row_in <= row_total and col_in <= col_total:
            for row in range(int(row_in), int(row_total)):
                try:
                    temp = int(self.__sheet_selected.col_values(int(col_in))[row])
                except ValueError:
                    temp = 0
                except:
                    temp = 0
                grade.append(temp)
            return grade
        return None

    @property
    def excel_name(self):
        return self.__excel_name

    @excel_name.setter
    def excel_name(self, excel_name):
        self.__excel_name = excel_name

    @property
    def excel_selected(self):
        return self.__excel_selected

    @property
    def sheet_list(self):
        return self.__sheet_list

    @property
    def sheet_name(self):
        return self.__sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name):
        self.__sheet_name = sheet_name

    @property
    def sheet_selected(self):
        return self.__sheet_selected

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
