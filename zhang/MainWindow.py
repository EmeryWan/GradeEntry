import copy
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from zhang import log
from zhang.ui.EntryWindow import Ui_MainWindow

logger = log.logger
logger.name = 'Main Window'


class ExcelReadThread(QThread):
    """
    接收　excel实例对象　row col
    读取成绩信息
    返回　成绩列表集合信号
    """
    grade_single_out = pyqtSignal(list)

    def __init__(self, parent=None, excel=None, row=None, col=None):
        super(ExcelReadThread, self).__init__(parent)
        # self.working = True
        self.excel = excel
        self.row = row
        self.col = col

    def __del__(self):
        # self.working = False
        self.wait()

    def set_excel(self, excel):
        self.excel = excel

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def run(self):
        """
        获得列表　返回信号
        :return:
        """
        # if self.working:
        info = self.excel.grade_info(row_in=self.row, col_in=self.col)
        self.grade_single_out.emit(info)


class BrowserFromEntryThread(QThread):
    """
    接收browser 对象
    查找页面form
    填充form
    """

    def __init__(self, parent=None, browser=None, grade_list=None):
        super(BrowserFromEntryThread, self).__init__(parent)
        # self.working = True
        self.browser = browser
        self.grade_list = grade_list

    def __del__(self):
        # self.working = False
        self.wait()

    def set_browser(self, browser):
        self.browser = browser

    def set_grade_list(self, grade_list):
        self.grade_list = grade_list

    def run(self):
        """
        执行填充动作
        """
        # if self.working:
        try:
            self.browser.start_entry_data(grade_list=self.grade_list)
        except:
            print("run diancuo")


class CheckboxThread(QThread):
    def __init__(self, parent=None, browser=None):
        super(CheckboxThread, self).__init__(parent)
        # self.working = True
        self.browser = browser

    def __del__(self):
        # self.working = False
        self.wait()

    def set_browser(self, browser):
        self.browser = browser

    def run(self):
        # if self.working:
        self.browser.click_all_checkbox()


class Window(QMainWindow):

    def __init__(self, browser, excel):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.browser_operate = browser
        self.excel_operate = excel
        # 要录入的成绩列表(线程中获得)
        self.grade_list = []

        # 开启窗体执行
        self.setFixedSize(self.width(), self.height())
        self.fill_excel_listWidget()

        # 控件的绑定和初始化
        self.ui.groupBox_advance.setVisible(False)
        self.ui.checkBox_advance.stateChanged.connect(self.set_advance_visible)
        self.ui.btn_re_view_excel.clicked.connect(self.fill_excel_listWidget)
        self.ui.btn_select_excel.clicked.connect(self.fill_sheet_comboBox)
        self.ui.comboBox_excel_sheet.currentTextChanged.connect(self.fill_row_col_info)  # combobox 当前选择改变时执行
        self.ui.btn_start.clicked.connect(self.start_entry)
        self.ui.btn_click_checkbox.clicked.connect(self.check_box)

        # 线程的初始化
        # self.excel_info_thread = ExcelReadThread(excel=self.excel_operate)
        # self.excel_info_thread.grade_single_out.connect(self.get_grade_info_thread)
        self.browser_entry_thread = BrowserFromEntryThread(browser=self.browser_operate)
        self.check_box_thread = CheckboxThread(browser=self.browser_operate)

    def get_grade_info_thread(self, g_list):
        """
        从线程中获得数据
        """
        self.grade_list = g_list

    def set_advance_visible(self):
        """
        控制高级选项
        """
        if self.ui.checkBox_advance.isChecked():
            self.ui.groupBox_advance.setVisible(True)
        else:
            self.ui.groupBox_advance.setVisible(False)

    # -------------------------------------------------------------------------

    def fill_excel_listWidget(self):
        """
        获得所有的excel，并填充到窗体列表
        """
        excel_list = self.excel_operate.get_all_excel()
        if excel_list is not None:
            self.ui.listWidget_excel_list.clear()
            self.ui.listWidget_excel_list.addItems(excel_list)
        else:
            # QMessage
            pass

    def fill_sheet_comboBox(self):
        """
        获得选定excel的sheet信息，并填充到窗体
        :return:
        """
        try:
            e_name = self.ui.listWidget_excel_list.currentItem()
            self.excel_operate.excel_name = str(e_name.text())
            self.excel_operate.get_all_sheets()
            sheet_list = self.excel_operate.sheet_list
            if sheet_list is not None:
                self.ui.comboBox_excel_sheet.clear()
                self.ui.comboBox_excel_sheet.addItem('请选择Sheet')
                self.ui.comboBox_excel_sheet.addItems(sheet_list)
            else:
                # QMessage
                pass
        except:
            pass

    def fill_row_col_info(self):
        """
        选择sheet后 更新窗体中row col
        对列(col)需要进行装换 1->A 27->AA
        :return:
        """
        try:  # 因为第一个是中文提示会报错　一定要try
            # -1 窗体预设值 0 修改后预设值
            print('out')
            print(self.ui.comboBox_excel_sheet.currentIndex())
            if self.ui.comboBox_excel_sheet.currentIndex() > 0:
                # 得到选择的sheet
                self.excel_operate.sheet_name = str(self.ui.comboBox_excel_sheet.currentText())
                print(self.excel_operate.sheet_name)
                # 获得行列信息
                row, col = self.excel_operate.row_col_length()
                # 将信息填进去
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

    def read_excel(self, row, col):
        print(len(self.grade_list))
        print(self.grade_list)
        if len(self.grade_list) != 0:
            self.grade_list.clear()
        # 无数据 []
        # 有数据 [1, 2, 3 ...]
        # 返回None 表示输入的行列超出了
        g_list = self.excel_operate.grade_info(row, col)
        if g_list is not None:
            # self.grade_list.copy()
            self.grade_list = copy.deepcopy(g_list)
        else:
            # QMessageBox
            pass

    def start_entry(self):
        """
        需要 读取 comboBox_excel_sheet comboBox_get_mode comboBox_get_row comboBox_get_col
        开始后将其他控件设置为不可用
        :return:
        """
        try:
            row = str(int(self.ui.comboBox_get_row.currentText()) - 1)
            col = str(int(colname_to_colnum(self.ui.comboBox_get_col.currentText())) - 1)
            print("start entry")
            print(row, " ", col)
            self.ui.btn_start.setEnabled(False)
            # 读取数据放入 self.grade_list
            self.read_excel(row, col)
            print("starrt")
            print(self.grade_list)
            self.start_browser_entry_thread()
            self.ui.btn_start.setEnabled(True)
        except:
            pass
        # 开始线程
        # self.start_excel_info_thread(row, col)
        # self.start_browser_entry_thread()
        #
        # self.ui.btn_select_excel.setEnabled(True)
        # self.grade_list.clear()

    def start_excel_info_thread(self, row, col):
        try:
            self.excel_info_thread.set_col(col)
            self.excel_info_thread.set_row(row)
            self.excel_info_thread.start()
            time.sleep(20)
            print('main windows start_excel_info_thread')
            print(self.grade_list)
            print("main windows")
        except:
            print("start_excel_info_thread")

    def start_browser_entry_thread(self):
        if len(self.grade_list) != 0:
            self.browser_entry_thread.set_grade_list(self.grade_list)
            self.browser_entry_thread.start()
            logger.info('填充线程执行完毕')
        else:
            logger.error('没有获取到成绩信息')

    # -----------------------------------------------------------------------------

    """
    高级选项
    """

    def start_check_box_thread(self):
        try:
            self.check_box_thread.start()
        except:
            print("点点点")

    def check_box(self):
        """
        填充页面的checkbox
        :return:
        """
        try:
            self.start_check_box_thread()
        except:
            # QMessageBox
            pass

    def change_page_control(self):
        pass

    def refresh_page_info(self):
        pass


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
            result += chr(temp + 65)
        else:
            result += chr(colnum % 26 - 1 + 65)
        colnum //= 26
    # 倒序输出拼写的字符串
    return result[::-1]
