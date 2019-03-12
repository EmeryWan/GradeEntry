import os

import xlrd as xlrd


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
        self.__sheet_name = None
        # 选择的sheet对象 sheet_by_name(sheet_names[sheet_name])
        self.__sheet_selected = None

    def find_all_excel(self):
        """
        将目录下的文件显示到框中
        """
        path = "..//excel"
        files = os.listdir(path)
        # self.excel_file_list.clear()
        for file in files:
            # 需要排除临时文件  .~20181-4.xlsx
            self.excel_file_list.append(file)
        return self.excel_file_list

    def get_sheets(self):
        print(self.__excel_name)
        # print(r"..//excel//" + self.__excel_name)
        self.__excel_selected = xlrd.open_workbook(r"..//excel//" + self.__excel_name)

        # ['平时成绩', 'Sheet2', '考核成绩']
        self.__sheet_list = self.__excel_selected.sheet_names()

    def row_col_length(self):
        self.__sheet_selected = self.__excel_selected.sheet_by_name(self.__sheet_name)
        # 显示行列数是以1开始，取值时以0开始
        row = self.__sheet_selected.nrows
        print("row: ", row)
        col = self.__sheet_selected.ncols
        print("col: ", col)
        return row, col

    def info(self, row_in, col_in):
        grade = []
        for row in range(row_in, len(self.__sheet_selected.ncols)):
            try:
                temp = int(self.__sheet_selected.col_values(col_in)[row])
            except ValueError:
                temp = 0
            except:
                temp = 0
            grade.append(temp)
        return grade

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


class SheetInfo:
    def __init__(self, sheet_name, row, col):
        self.__sheet_selected = sheet_name
        self.__row = row
        self.__col = col


if __name__ == '__main__':
    e = Excel()
    print(e.excel_file_list)
    e.excel_name = "20181-4.xlsx"
    e.get_sheets()
    print(e.sheet_list)
    e.sheet_name = "平时成绩"
    r, c = e.row_col_length()
    print(r, c)
    print(e.sheet_selected.cell(rowx=5, colx=1).value)
    print(e.sheet_selected.cell(rowx=26, colx=26).value)
