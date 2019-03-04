import os

from PyQt5.QtWidgets import QMainWindow

from zhang.EntryWindow import Ui_MainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 开启要执行的动作
        self.get_all_excel()

        # 控件操作
        self.ui.groupBox_advance.setVisible(False)
        self.ui.checkBox_advance.stateChanged.connect(self.set_advance_visible)
        self.ui.btn_re_view_excel.clicked.connect(self.get_all_excel)
        self.ui.btn_select_excel.clicked.connect(self.get_this_excel)
        self.ui.comboBox_excel_sheet.currentIndexChanged.connect(self.get_row_col_info())

    def set_advance_visible(self):
        """ 设置高级是否可见 """
        if self.ui.checkBox_advance.isChecked():
            self.ui.groupBox_advance.setVisible(True)
        else:
            self.ui.groupBox_advance.setVisible(False)

    def get_all_excel(self):
        """ 获得所有的excel """
        path = "..\\excel\\"
        files = os.listdir(path)
        print(files)
        self.ui.listWidget_excel_list.clear()
        for file in files:
            print(file)
            self.ui.listWidget_excel_list.addItem(str(file))

    def get_this_excel(self):
        """ 选择要的excel 更新sheet部分 """
        try:
            # 选择excel
            excel_name = self.ui.listWidget_excel_list.currentItem()
            # 读取并获得sheet信息
            sheet_list = ['1', '2', '3']
            # 将sheet信息写到控件
            self.ui.comboBox_excel_sheet.addItems(sheet_list)
        except:
            print("qqq")

    def get_row_col_info(self):
        """ 选择sheet 更新 row col """

        # 得到选择的sheet

        # 获得行列信息
        row = 17
        col = 18
        # 将信息填进去
        for i in range(17):
            self.ui.comboBox_get_row.addItem(str(i+1))

    def start_entry(self):
        """
        需要 读取 comboBox_excel_sheet comboBox_get_mode comboBox_get_row comboBox_get_col
        开始后将其他控件设置为不可用
        :return:
        """
        # 读取行列数据
        # 调用方法 获得数据
        # 向浏览器页面填充数据
        pass


    """
    高级部分
    """
    def check_box(self):
        pass

    def change_page_control(self):
        pass

    def refresh_page_info(self):
        pass


def num_to_char(number):
    factor, moder = divmod(number, 26)
    mod_char = chr(moder + 65)
    if factor != 0:
        mod_char = num_to_char(factor - 1) + mod_char
    return mod_char