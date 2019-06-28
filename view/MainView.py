import os
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from ui.MainWindow import Ui_MainWindow

from controller.BrowserController import BrowserController
from controller.ExcelController import ExcelController

from singleton.AboutViewSingleton import AboutViewSingle
from singleton.MapViewSingleton import MapViewSingleton

from util import Tool
from util.Configuration import SettingsInfo, ECJTU_MAIN_LOGO_PATH, ECJTU_ICON_LOGO_PATH, LOG_ERROR_TEMPLATE, \
    LOG_INFO_TEMP
from util.LevelSystem import LevelSystemEnum
from util.Log import LoggerSingleton, Logger

# final
##########################################
SHEET_COMBOBOX_INIT_ITEM = "请先选择Excel文件"
R_C_COMBOBOX_INIT_ITEM = "先选择Excel"
COMBOBOX_TIP_SELECT_SHEET_ITEM = "请先选择页"
COMBOBOX_TIP_SELECT_ROW_ITEM = "请选择__行"
COMBOBOX_TIP_SELECT_COL_ITEM = "请选择__列"

# message box
MESSAGE_BOX_TITLE_EXIT = "退出"
MESSAGE_BOX_TITLE_ERROR = "错误"
MESSAGE_BOX_TITLE_WARNING = "警告"
MESSAGE_BOX_TITLE_ENSURE = "请确定"

MESSAGE_BOX_EXIT_INFO = "注意！关闭程序后浏览器也会关闭！"
MESSAGE_BOX_NO_FILE_INFO = "不能读取文件（文件夹下Excel或没有权限读取）"
MESSAGE_BOX_NO_EXCEL_INFO = "没有该Excel信息，请先录入其他文件"
MESSAGE_BOX_START_INFO = "录入成绩会占用鼠标键盘\n\n完毕前请不要使用鼠标键盘"
MESSAGE_BOX_RE_BROWSER_INFO = "请确定浏览器被误关闭后再继续"
MESSAGE_BOX_THREAD_ERROR_INFO = "程序线程错误"
MESSAGE_BOX_ERROR_PAGE_INFO = "请到正确的操作页面！"
MESSAGE_BOX_CLEAN_PAGE_INFO = "该项只对百分制录入页面有效"

FILE_DIALOG_INFO = "华东交通大学 - 成绩录入辅助软件 - 请选需要存放Excel的文件夹"


class ReReadExcelInfoThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ReReadExcelInfoThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        sign = ExcelController.read_target_dir_info()
        self.signal_out.emit(sign)


class ReOpenBrowserThread(QThread):
    def __init__(self, parent=None):
        super(ReOpenBrowserThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        BrowserController.close_browser()
        time.sleep(0.2)
        BrowserController.open_website()


class BrowserFromEntryThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None, level=None, grade_list=None):
        super(BrowserFromEntryThread, self).__init__(parent)
        self.level = level
        self.grade_list = grade_list

    def __del__(self):
        self.wait()

    def set_level(self, level):
        self.level = level

    def set_grade_list(self, grade_list):
        self.grade_list = grade_list

    def run(self):
        sign = BrowserController.start_entry_data(sign=self.level, grade_list=self.grade_list)
        self.signal_out.emit(sign)


class CheckboxThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(CheckboxThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        sign = BrowserController.click_all_checkbox()
        self.signal_out.emit(sign)


class CleanInputThread(QThread):
    def __init__(self, parent=None):
        super(CleanInputThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        BrowserController.clean_input()


########################################


class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # 数据
        # {sheetName -> {row:, col:}}  key: sheet 名  value: 行列map
        self.__request_excel_name = None
        self.__request_excel_sheet_name = None
        self.__request_view_info = None

        # 线程的初始化
        self.__re_read_excel_thread = ReReadExcelInfoThread()
        self.__re_read_excel_thread.signal_out.connect(self.__read_excel_thread_signal)
        self.__browser_entry_thread = BrowserFromEntryThread()
        self.__browser_entry_thread.signal_out.connect(self.__page_not_find_thread_signal)
        self.__check_box_thread = CheckboxThread()
        self.__check_box_thread.signal_out.connect(self.__page_not_find_thread_signal)
        self.__clean_input_thread = CleanInputThread()
        self.__re_open_browser_thread = ReOpenBrowserThread()

        # 初始化
        self.__init_all()

    ####################################

    def __init_all(self):
        try:
            self.__window_init()
            self.__level_init()
            self.__logo_init()
            self.__init_fill_excel_listWighet()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __window_init(self):
        try:
            # 控件的可见性 可用性
            self.ui.groupBox_advance.setVisible(False)

            # 高级选项
            self.ui.checkBox_advance.stateChanged.connect(self.__set_advance_visible)
            # 刷新按钮
            self.ui.btn_re_view_excel.clicked.connect(self.__fill_excel_listWidget)
            # 打开文件夹按钮
            self.ui.btn_open_dir.clicked.connect(self.__set_new_excel_dir)

            # 选择按钮
            self.ui.btn_select_excel.clicked.connect(self.__fill_sheet_comboBox)
            self.ui.listWidget_excel_list.currentItemChanged.connect(self.__fill_sheet_comboBox)
            # combobox 当前选择改变时执行 填充 行列
            self.ui.comboBox_excel_sheet.currentTextChanged.connect(self.__fill_row_col_info)

            # 开始按钮
            self.ui.btn_start.clicked.connect(self.__start_entry)
            # check_box
            self.ui.btn_click_checkbox.clicked.connect(self.__check_box)
            # 联系
            self.ui.commandLinkButton_feedback.clicked.connect(self.__feedback)
            # 重新打开浏览器
            self.ui.btn_re_open_browser.clicked.connect(self.__re_open_browser)
            # 清除日志
            self.ui.btn_clean_log.clicked.connect(self.__clean_log_file)
            # map
            self.ui.btn_map.clicked.connect(self.__level_map_view)
            # 清除输入
            self.ui.btn_clean_input.clicked.connect(self.__clean_input)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __level_init(self):
        """ 初始化等级框 """
        self.ui.level_comboBox.addItem(str(LevelSystemEnum.HUNDRED.value))
        self.ui.level_comboBox.addItem(str(LevelSystemEnum.FIVE.value))
        self.ui.level_comboBox.addItem(str(LevelSystemEnum.TWO.value))

    def __logo_init(self):
        try:
            self.ui.ecjtu_logo_label.setPixmap(QPixmap(ECJTU_MAIN_LOGO_PATH))
            self.ui.ecjtu_logo_label.setScaledContents(True)
            self.setWindowIcon(QIcon(ECJTU_ICON_LOGO_PATH))
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __reset_window_control(self):
        """
        重置控件 主要是下拉列表
        """
        self.ui.comboBox_excel_sheet.clear()
        self.ui.comboBox_get_row.clear()
        self.ui.comboBox_get_col.clear()
        self.ui.comboBox_excel_sheet.addItem(SHEET_COMBOBOX_INIT_ITEM)
        self.ui.comboBox_get_row.addItem(R_C_COMBOBOX_INIT_ITEM)
        self.ui.comboBox_get_col.addItem(R_C_COMBOBOX_INIT_ITEM)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, MESSAGE_BOX_TITLE_EXIT, MESSAGE_BOX_EXIT_INFO,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            BrowserController.close_browser()
            event.accept()
        else:
            event.ignore()

    def __set_advance_visible(self):
        if self.ui.checkBox_advance.isChecked():
            self.ui.groupBox_advance.setVisible(True)
            self.ui.groupBox_about_info.setVisible(False)
        else:
            self.ui.groupBox_advance.setVisible(False)
            self.ui.groupBox_about_info.setVisible(True)

    # 上面是控件的操作
    #################################

    def __init_fill_excel_listWighet(self):
        try:
            # 获得所有的 excel 名
            excel_list = ExcelController.get_excel_list()
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(excel_list)))
            # 填充
            if len(excel_list) > 0:
                self.ui.listWidget_excel_list.clear()
                self.ui.listWidget_excel_list.addItems(excel_list)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __set_new_excel_dir(self):
        try:
            current_path = os.getcwd()
            excel_dir_path = QFileDialog.getExistingDirectory(self, FILE_DIALOG_INFO, current_path)
            if excel_dir_path is not None and "" != excel_dir_path:
                # 更新目录 调用方法 读取文件
                SettingsInfo.EXCEL_FILES_PATH = excel_dir_path
                ExcelController.read_target_dir_info()
                # 清除旧显示 显示新内容
                self.ui.listWidget_excel_list.clear()
                self.__fill_excel_listWidget()
                # 重置控件
                self.__reset_window_control()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __fill_excel_listWidget(self):
        try:
            excel_list = ExcelController.get_excel_list()
            if len(excel_list) == 0:
                QMessageBox.question(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_NO_FILE_INFO, QMessageBox.Yes,
                                     QMessageBox.Yes)
                self.__set_new_excel_dir()
            if excel_list is not None and len(excel_list) > 0:
                self.ui.listWidget_excel_list.clear()
                self.ui.listWidget_excel_list.addItems(excel_list)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    # 点击选择按钮 触发该事件
    def __fill_sheet_comboBox(self):
        try:
            # 如果combobox 长度为0
            if self.ui.listWidget_excel_list.count() == 0:
                return

            try:
                # 获得选择的 excel
                excel_item = self.ui.listWidget_excel_list.currentItem()
            except BaseException:
                return

            excel_name = str(excel_item.text()).strip()
            self.__request_excel_name = excel_name

            # 在label上显示选择的excel名
            self.ui.cur_excel_name_label.setText(excel_name)

            # { sheetName -> {row:, col:}, ... } key: sheet名, value: 行列map
            view_info = ExcelController.get_view_info_by_name(excel_name)
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(view_info)))
            if view_info is None:
                QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_NO_EXCEL_INFO, QMessageBox.Yes,
                                    QMessageBox.Yes)
                return

            self.__request_view_info = view_info
            sheet_list = list(view_info.keys())
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(sheet_list)))
            if sheet_list is not None:
                self.ui.comboBox_excel_sheet.clear()
                self.ui.comboBox_excel_sheet.addItem(COMBOBOX_TIP_SELECT_SHEET_ITEM)
                self.ui.comboBox_excel_sheet.addItems(sheet_list)
                self.ui.comboBox_get_row.clear()
                self.ui.comboBox_get_row.addItem(COMBOBOX_TIP_SELECT_SHEET_ITEM)
                self.ui.comboBox_get_col.clear()
                self.ui.comboBox_get_col.addItem(COMBOBOX_TIP_SELECT_SHEET_ITEM)
            else:
                QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_NO_EXCEL_INFO, QMessageBox.Yes,
                                    QMessageBox.Yes)

        except:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __fill_row_col_info(self):
        # 因为第一个是中文提示会报错　一定要try
        try:
            # -1 窗体预设值 0 修改后预设值
            if self.ui.comboBox_excel_sheet.currentIndex() <= 0:
                self.ui.comboBox_get_row.clear()
                self.ui.comboBox_get_col.clear()

            if self.ui.comboBox_excel_sheet.currentIndex() > 0:
                # 得到选择的sheet
                this_sheet_name = str(self.ui.comboBox_excel_sheet.currentText()).strip()
                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(this_sheet_name)))
                self.__request_excel_sheet_name = this_sheet_name

                row_col_map = self.__request_view_info.get(this_sheet_name)
                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(row_col_map)))
                row = row_col_map["row"]
                col = row_col_map["col"]

                if row != 0 and col != 0:
                    self.ui.comboBox_get_row.clear()
                    self.ui.comboBox_get_row.addItem(COMBOBOX_TIP_SELECT_ROW_ITEM)
                    self.ui.comboBox_get_col.clear()
                    self.ui.comboBox_get_col.addItem(COMBOBOX_TIP_SELECT_COL_ITEM)
                    for i in range(row):
                        self.ui.comboBox_get_row.addItem(str(i + 1))
                    for j in range(col):
                        self.ui.comboBox_get_col.addItem(Tool.colnum_to_colname(str(j + 1)))
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __get_grade_list(self):
        try:
            # 集合信息
            excel_name = self.__request_excel_name
            sheet_name = self.__request_excel_sheet_name
            row = str(int(self.ui.comboBox_get_row.currentText()) - 1)
            col = str(int(Tool.colname_to_colnum(self.ui.comboBox_get_col.currentText())) - 1)

            grade_info_list = ExcelController.get_grade_info_by_col(excel_name, sheet_name, row, col)
            return grade_info_list
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            return []

    def __start_entry(self):

        reply = QMessageBox.question(self, MESSAGE_BOX_TITLE_ENSURE, MESSAGE_BOX_START_INFO,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # 获得成绩 等级
                grade_info_list = self.__get_grade_list()
                level = self.ui.level_comboBox.currentText().strip()

                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(grade_info_list)))
                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), str(level)))

                if len(grade_info_list) > 0 and grade_info_list is not None:
                    self.__start_browser_entry_thread(level, grade_info_list)
                else:
                    QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_NO_EXCEL_INFO, QMessageBox.Yes,
                                        QMessageBox.Yes)
            except BaseException:
                LoggerSingleton.instance().error(
                    LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __check_box(self):
        # 添加一个判断是否在指定页面
        try:
            reply = QMessageBox.question(self, MESSAGE_BOX_TITLE_ENSURE, MESSAGE_BOX_START_INFO,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.__start_check_box_thread()

        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __clean_input(self):
        try:
            reply = QMessageBox.question(self, MESSAGE_BOX_TITLE_ENSURE, MESSAGE_BOX_CLEAN_PAGE_INFO,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.__start_clean_input_thread()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    # 下栏
    ################################

    def __feedback(self):
        AboutViewSingle.instance().show()

    def __re_open_browser(self):
        try:
            reply = QMessageBox.question(self, MESSAGE_BOX_TITLE_ENSURE, MESSAGE_BOX_RE_BROWSER_INFO,
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.__start_re_browser_thread()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __clean_log_file(self):
        try:
            Logger.clean_log_file()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __level_map_view(self):
        MapViewSingleton.instance().show()

    # 线程
    #######################################################################

    def __start__excel_thread(self):
        try:
            if not self.__re_read_excel_thread.isRunning():
                self.__re_read_excel_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __start_browser_entry_thread(self, level, grade_list):
        try:
            self.__browser_entry_thread.set_level(level)
            self.__browser_entry_thread.set_grade_list(grade_list)
            self.__browser_entry_thread.start()
        except:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_THREAD_ERROR_INFO, QMessageBox.Yes,
                                QMessageBox.Yes)

    def __start_check_box_thread(self):
        try:
            self.__check_box_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_THREAD_ERROR_INFO, QMessageBox.Yes,
                                QMessageBox.Yes)

    def __start_clean_input_thread(self):
        try:
            self.__clean_input_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_THREAD_ERROR_INFO, QMessageBox.Yes,
                                QMessageBox.Yes)

    def __start_re_browser_thread(self):
        try:
            self.__re_open_browser_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_THREAD_ERROR_INFO, QMessageBox.Yes,
                                QMessageBox.Yes)

    def __read_excel_thread_signal(self, signal):
        if not signal:
            QMessageBox.warning(self, MESSAGE_BOX_TITLE_ERROR, MESSAGE_BOX_NO_FILE_INFO, QMessageBox.Yes,
                                QMessageBox.Yes)

    def __page_not_find_thread_signal(self, sign):
        if not sign:
            QMessageBox.warning(self, MESSAGE_BOX_TITLE_WARNING, MESSAGE_BOX_ERROR_PAGE_INFO, QMessageBox.Yes,
                                QMessageBox.Yes)
