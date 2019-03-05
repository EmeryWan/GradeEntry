import os

import xlrd as xlrd

excel_file_list = []
name_course = []


def find_excel_file():
    """
    将目录下的文件显示到框中
    """
    path = os.getcwd() + "..//excel"
    files = os.listdir(path)
    for file in files:
        excel_file_list.append(file)
    return excel_file_list


def sheet_info(name):
    """
    通过名字打开一个Excel
    返回excel的sheet名 显示到下拉列表
    """
    global use_excel

    use_excel= xlrd.open_workbook(os.getcwd() + "\\file\\" + name)
    # ['平时成绩', 'Sheet2', '考核成绩']
    sheet_names = use_excel.sheet_names()
    return sheet_names


def row_col_info(sheet_name):
    """
    通过选择的sheet 获取行列信息显示到下拉列表
    """
    global sheet_selected

    sheet_selected = use_excel.sheet_by_name(sheet_name)

    global row
    global col

    row = sheet_selected.nrows
    col = sheet_selected.ncols
    return row, col

def grade_info(selected_row, selected_col, mode):
    start_row = selected_row - 1
    start_col = selected_col - 1

    if len(name_course) > 0:
        name_course.clear()
