import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from zhang import log
from zhang.ui.EntryWindow import Ui_MainWindow

logger = log.logger


class ExcelReadThread(QThread):
    """
    接收　excel实例对象　row col
    读取成绩信息
    返回　成绩列表集合信号
    """
    grade_single_out = pyqtSignal(list)

    def __init__(self, parent=None, excel=None, row=None, col=None):
        super(ExcelReadThread, self).__init__(parent)
        self.working = True
        self.excel = excel
        self.row = row
        self.col = col

    def __del__(self):
        self.working = False
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
        # [] 分数列表
        info = self.excel.info(row_in=self.row, col_in=self.col)
        print('thread :', info)
        self.grade_single_out.emit(info)


class BrowserFromEntryThread(QThread):
    """
    接收browser 对象
    查找页面form
    填充form
    """

    def __init__(self, parent=None, browser=None, grade_list=None):
        super(BrowserFromEntryThread, self).__init__(parent)
        self.working = True
        self.browser = browser
        self.grade_list = grade_list

    def __del__(self):
        self.working = False
        self.wait()

    def set_browser(self, browser):
        self.browser = browser

    def set_grade_list(self, grade_list):
        self.grade_list = grade_list

    def run(self):
        """
        执行填充动作
        """
        self.browser.start_entry_data(grade_list=self.grade_list)


class Window(QMainWindow):

    def __init__(self, browser, excel):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.browser = browser
        self.excel = excel
        # path = r"..//config//chromedriver"
        # option = webdriver.ChromeOptions()
        # option.add_argument('disable-infobars')
        # self.brow = webdriver.Chrome(executable_path=path, options=option)

        self.grade_list = []

        # 开启要执行的动作
        self.setFixedSize(self.width(), self.height())
        self.get_all_excel()

        # 控件操作
        self.ui.groupBox_advance.setVisible(False)
        # self.setFixedSize(self.width(), self.height() - 180)
        self.ui.checkBox_advance.stateChanged.connect(self.set_advance_visible)
        self.ui.btn_re_view_excel.clicked.connect(self.get_all_excel)
        self.ui.btn_select_excel.clicked.connect(self.fill_sheet_comboBox)
        self.ui.comboBox_excel_sheet.currentTextChanged.connect(self.get_row_col_info)
        self.ui.btn_start.clicked.connect(self.start_entry)

        # 线程
        self.excel_info_thread = ExcelReadThread(excel=excel)
        self.excel_info_thread.grade_single_out.connect(self.get_info)
        self.browser_entry_thread = BrowserFromEntryThread(browser=browser)

    def get_info(self, grade_list):
        print(grade_list)
        self.grade_list = grade_list

    def set_advance_visible(self):
        """ 设置高级是否可见 """
        if self.ui.checkBox_advance.isChecked():
            self.ui.groupBox_advance.setVisible(True)
            # self.setFixedSize(self.width(), self.height() + 180)
        else:
            # self.setFixedSize(self.width(), self.height() - 180)
            self.ui.groupBox_advance.setVisible(False)

    def get_all_excel(self):
        """ 获得所有的excel """
        excel_list = self.excel.excel_file_list
        self.ui.listWidget_excel_list.clear()
        self.ui.listWidget_excel_list.addItems(excel_list)

    def fill_sheet_comboBox(self):
        e_name = self.ui.listWidget_excel_list.currentItem()
        print(e_name)
        print(e_name.text())
        self.excel.excel_name = e_name.text()
        self.excel.get_sheets()
        sheet_list = self.excel.sheet_list
        print(sheet_list)
        self.ui.comboBox_excel_sheet.clear()
        self.ui.comboBox_excel_sheet.addItem('请选择Sheet')
        self.ui.comboBox_excel_sheet.addItems(sheet_list)

    def choose_this_excel(self):
        """ 选择要的excel 更新sheet部分 """
        try:
            # 选择excel
            excel_name = self.ui.listWidget_excel_list.currentItem()
            # 读取并获得sheet信息
            sheet_list = ['1', '2', '3']
            # 将sheet信息写到控件
            self.ui.comboBox_excel_sheet.clear()
            self.ui.comboBox_excel_sheet.addItem('请选择Sheet')
            self.ui.comboBox_excel_sheet.addItems(sheet_list)
        except:
            print("qqq")

    def get_row_col_info(self):
        """ 选择sheet 更新 row col """
        try:  # 因为第一个是中文提示会报错　一定要try
            print(self.ui.comboBox_excel_sheet.currentIndex())
            if self.ui.comboBox_excel_sheet.currentIndex() != -1:
                # 得到选择的sheet
                sheet_selected = self.ui.comboBox_excel_sheet.currentText()
                print(sheet_selected)
                self.excel.sheet_name = str(sheet_selected)
                # 获得行列信息
                row, col = self.excel.row_col_length()
                # 将信息填进去
                self.ui.comboBox_get_row.clear()
                self.ui.comboBox_get_row.addItem('选择行')
                self.ui.comboBox_get_col.clear()
                self.ui.comboBox_get_col.addItem('选择列')
                for i in range(row):
                    self.ui.comboBox_get_row.addItem(str(i))
                for j in range(col):
                    self.ui.comboBox_get_col.addItem(str(j))
        except:
            pass

    def start_entry(self):
        """
        需要 读取 comboBox_excel_sheet comboBox_get_mode comboBox_get_row comboBox_get_col
        开始后将其他控件设置为不可用
        :return:
        """
        # 读取行列数据
        # 调用方法 获得数据
        # 向浏览器页面填充数据
        row = self.ui.comboBox_get_row.currentText()
        col = self.ui.comboBox_get_col.currentText()
        sheet = self.ui.comboBox_excel_sheet
        print('start: ', col, ' ', row)
        self.ui.btn_start.setEnabled(False)
        self.start_excel_info_thread(row, col)
        self.start_browser_thread()

    def start_excel_info_thread(self, row, col):
        self.excel_info_thread.set_col(col)
        self.excel_info_thread.set_row(row)
        self.excel_info_thread.start()

    def start_browser_thread(self):
        self.browser_entry_thread.start()

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
