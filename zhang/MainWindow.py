import copy
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from zhang import log
from zhang.BrowserOperate import BrowserOperate
from zhang.EntryWindow import Ui_MainWindow

logger = log.logger
logger.name = 'Main Window'


class BrowserFromEntryThread(QThread):
    def __init__(self, parent=None, grade_list=None):
        super(BrowserFromEntryThread, self).__init__(parent)
        self.grade_list = grade_list

    def __del__(self):
        self.wait()

    def set_grade_list(self, grade_list):
        self.grade_list = grade_list

    def run(self):
        try:
            BrowserOperate.start_entry_data(grade_list=self.grade_list)
        except:
            print("run diancuo")


class CheckboxThread(QThread):
    def __init__(self, parent=None):
        super(CheckboxThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        BrowserOperate.click_all_checkbox()


class Window(QMainWindow):

    def __init__(self, excel_operator):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.excel_operate = excel_operator

        self.window_init()
        self.fill_excel_listWidget()

        # 线程的初始化
        self.browser_entry_thread = BrowserFromEntryThread()
        self.check_box_thread = CheckboxThread()
        # 数据暂存
        self.request_excel_object = None
        self.request_excel_sheet_name = None

    def window_init(self):
        # 控件的可见性 可用性
        self.ui.groupBox_advance.setVisible(False)
        # self.ui.btn_start.setEnabled(False)
        # self.ui.btn_click_checkbox.setEnabled(False)

        # 控件的绑定和初始化
        self.ui.checkBox_advance.stateChanged.connect(self.set_advance_visible)
        self.ui.btn_re_view_excel.clicked.connect(self.fill_excel_listWidget)
        self.ui.btn_select_excel.clicked.connect(self.fill_sheet_comboBox)
        self.ui.comboBox_excel_sheet.currentTextChanged.connect(self.fill_row_col_info)  # combobox 当前选择改变时执行
        self.ui.btn_start.clicked.connect(self.start_entry)
        self.ui.btn_click_checkbox.clicked.connect(self.check_box)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', '确定要退出程序？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 关闭浏览器
            event.accept()
        else:
            event.ignore()

    def set_advance_visible(self):
        if self.ui.checkBox_advance.isChecked():
            self.ui.groupBox_advance.setVisible(True)
        else:
            self.ui.groupBox_advance.setVisible(False)

    def fill_excel_listWidget(self):
        excel_list = self.excel_operate.get_all_excel_name_lists()
        if excel_list is not None:
            if len(excel_list) == 0:
                QMessageBox.warning(self, '没有文件', '该路径下没有读取到Excel文件\n请再确认一下', QMessageBox.Yes, QMessageBox.Yes)

            self.ui.listWidget_excel_list.clear()
            self.ui.listWidget_excel_list.addItems(excel_list)
        else:
            QMessageBox.question(self, '问题', '不能读取该路径下的文件', QMessageBox.Yes, QMessageBox.Yes)

    def fill_sheet_comboBox(self):

        excel_item = self.ui.listWidget_excel_list.currentItem()
        excel_name = str(excel_item.text()).strip()
        print(excel_name)
        self.excel_operate.get_all_info(excel_name)
        print("@@111")
        self.request_excel_object = self.excel_operate.get_excel_object_info(excel_name)
        print('@@222')
        sheet_list = self.request_excel_object.sheet_lists
        if sheet_list is not None:
            self.ui.comboBox_excel_sheet.clear()
            self.ui.comboBox_excel_sheet.addItem('请选择Sheet')
            self.ui.comboBox_excel_sheet.addItems(sheet_list)
        else:
            # QMessage
            pass

    def fill_row_col_info(self):
        # 因为第一个是中文提示会报错　一定要try
        try:
            # -1 窗体预设值 0 修改后预设值
            if self.ui.comboBox_excel_sheet.currentIndex() <= 0:
                self.ui.comboBox_get_row.clear()
                self.ui.comboBox_get_col.clear()

            if self.ui.comboBox_excel_sheet.currentIndex() > 0:
                # 得到选择的sheet
                this_sheet_name = str(self.ui.comboBox_excel_sheet.currentText())
                self.request_excel_sheet_name = this_sheet_name

                row_col_map = self.request_excel_object.get_sheet_row_col(this_sheet_name)
                row = row_col_map['row']
                col = row_col_map['col']

                if row != 0 and col != 0:
                    self.ui.comboBox_get_row.clear()
                    self.ui.comboBox_get_row.addItem('请选择行')
                    self.ui.comboBox_get_col.clear()
                    self.ui.comboBox_get_col.addItem('请选择列')
                    for i in range(row):
                        self.ui.comboBox_get_row.addItem(str(i + 1))
                    for j in range(col):
                        self.ui.comboBox_get_col.addItem(colnum_to_colname(str(j + 1)))
                else:
                    # QMessageBox
                    pass
        except:
            pass

    def get_grade_info_list(self):

        excel_name = self.request_excel_object.excel_name
        sheet_name = self.request_excel_sheet_name

        row = str(int(self.ui.comboBox_get_row.currentText()) - 1)
        col = str(int(colname_to_colnum(self.ui.comboBox_get_col.currentText())) - 1)

        grade_info_list = self.excel_operate.get_grade_info(excel_name, sheet_name, row, col)
        return grade_info_list

    def start_entry(self):

        try:
            grade_info_list = self.get_grade_info_list()
            if len(grade_info_list) > 0:
                self.start_browser_entry_thread(grade_info_list)
            else:
                # QmessageBox
                pass
        except:
            pass

    def check_box(self):
        try:
            self.start_check_box_thread()
        except:
            # QMessageBox
            pass

    def start_browser_entry_thread(self, grade_info_list):
        self.browser_entry_thread.set_grade_list(grade_info_list)
        self.browser_entry_thread.start()

    def start_check_box_thread(self):
        try:
            self.check_box_thread.start()
        except:
            print("点点点")


def colname_to_colnum(colname):
    if type(colname) is not str:
        return colname
    col = 0
    power = 1
    for i in range(len(colname) - 1, -1, -1):
        ch = colname[i]
        col += (ord(ch) - ord('A') + 1) * power
        power *= 26
    return col


def colnum_to_colname(colnum):
    if not str(colnum).isdigit():
        return colnum
    colnum = int(colnum)
    result = ''
    while not (colnum // 26 == 0 and colnum % 26 == 0):
        temp = 25
        if colnum % 26 == 0:
            result += chr(temp + ord('A'))
        else:
            result += chr(colnum % 26 - 1 + ord('A'))
        if colnum % 26 == 0:
            colnum //= 26
            colnum -= 1
        else:
            colnum //= 26
    # 倒序输出拼写的字符串
    return result[::-1]
