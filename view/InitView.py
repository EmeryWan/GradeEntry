import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from controller.BrowserController import BrowserController
from controller.ExcelController import ExcelController
from singleton.DownloadViewSingleton import DownloadViewSingleton
from singleton.MainViewSingleton import MainViewSingleton
from ui.InitWindow import Ui_InItDialog
from util import Tool
from util.Configuration import SettingsInfo, ECJTU_MAIN_LOGO_PATH, ECJTU_ICON_LOGO_PATH, LOG_ERROR_TEMPLATE, \
    LOG_INFO_TEMP
from util.Log import LoggerSingleton

##############################

# final

NULL_STR = ""
BROWSER_TOOL_TIP = "点击打开浏览器"
EXCEL_TOOL_TIP = "点击选择读取Excel的文件夹"
ADVANCE_TIP = "提示：右键Chrome图标，点击打开所在位置可快速找到 （目录被隐藏请粘贴或手动输入）"
PATH_SELECT_TIP = "请选择到 如：C:\\Users\\zhangwei\\AppData\\Local\\Google\\Chrome\\Application"
ERROR_PATH_TIP = "路径选择错误！"

MESSAGE_BOX_TITLE_EXIT = "退出"
MESSAGE_BOX_EXIT_INFO = "注意！关闭程序后浏览器也会关闭！"

FILE_DIALOG_INFO = "华东交通大学 - 成绩录入辅助软件 - 请选需要存放Excel的文件夹"
PATH_DIALOG_INFO = "请选择 chrome.exe 的安装路径"

EXCEL_THREAD_FINISH_TIP = "读取Excel信息完毕"
BROWSER_THREAD_FINISH_TIP = "成功打开浏览器"
BROWSER_THREAD_ERROR_TIP = "无法打开浏览器\n开始下载驱动"
DRIVER_DOWNLOAD_FINISH_TIP = "驱动下载完毕 请再次打开"

OPEN_DEFAULT_PATH = os.path.join(os.getcwd(), "..")


##############################

# 读取文件线程
class ReadExcelInfoThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ReadExcelInfoThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        sign = ExcelController.read_target_dir_info()
        self.signal_out.emit(sign)


# 打开浏览器线程
class OpenBrowserThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(OpenBrowserThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        sign = BrowserController.re_open_browser()
        if sign:
            self.signal_out.emit(True)
        else:
            self.signal_out.emit(False)


##############################

class InitView(QDialog):
    def __init__(self):
        super(InitView, self).__init__()
        self.ui = Ui_InItDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # 标志
        self._browser_is_open_bool = False
        self._excel_path_is_select_bool = False

        # logo
        self.__show_icon()

        # 控件
        self.__init_config()

        # 线程初始化
        self.__excel_thread = ReadExcelInfoThread()
        self.__browser_thread = OpenBrowserThread()
        self.__excel_thread.signal_out.connect(self.__excel_thread_signal)
        self.__browser_thread.signal_out.connect(self.__browser_thread_signal)

    def __init_config(self):
        self.ui.btn_change_path.setVisible(False)
        self.ui.label_curr_chrome_path.setText("")
        self.ui.label_curr_chrome_path.setVisible(False)
        # 控件初始化
        self.ui.tip_label.setText(NULL_STR)
        self.ui.btn_open_browser.setToolTip(BROWSER_TOOL_TIP)
        self.ui.btn_select_excel.setToolTip(EXCEL_TOOL_TIP)

        # 事件绑定
        self.ui.btn_open_browser.clicked.connect(self.__open_browser)
        self.ui.btn_select_excel.clicked.connect(self.__select_excel_path)
        self.ui.btn_show_main_window.clicked.connect(self.__show_main_view)
        self.ui.checkBox.clicked.connect(self.__show_advance)
        self.ui.btn_change_path.clicked.connect(self.__chang_path)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, MESSAGE_BOX_TITLE_EXIT, MESSAGE_BOX_EXIT_INFO,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 关闭浏览器
            BrowserController.close_browser()
            event.accept()
        else:
            event.ignore()

    def __show_icon(self):
        try:
            self.ui.logo_label.setPixmap(QPixmap(ECJTU_MAIN_LOGO_PATH))
            self.ui.logo_label.setScaledContents(True)
            self.setWindowIcon(QIcon(ECJTU_ICON_LOGO_PATH))
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    ##############################

    def __open_browser(self):
        try:
            self.__start_browser_thread()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __select_excel_path(self):
        try:
            excel_dir_path = QFileDialog.getExistingDirectory(self, FILE_DIALOG_INFO, OPEN_DEFAULT_PATH)
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), excel_dir_path))
            if excel_dir_path is not None and NULL_STR != excel_dir_path:
                SettingsInfo.EXCEL_FILES_PATH = excel_dir_path
            self.__start_excel_thread()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __start_excel_thread(self):
        try:
            if not self.__excel_thread.isRunning():
                self.__excel_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __start_browser_thread(self):
        try:
            if not self.__browser_thread.isRunning():
                self.__browser_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __excel_thread_signal(self, signal):
        if signal:
            self._excel_path_is_select_bool = True
            self.__show_message(EXCEL_THREAD_FINISH_TIP)
        self.__auto_show_main_view()

    def __browser_thread_signal(self, signal):
        if signal:
            self.__show_message(BROWSER_THREAD_FINISH_TIP)
            self._browser_is_open_bool = True
            self.ui.btn_show_main_window.setEnabled(True)
        else:
            self.__show_message(BROWSER_THREAD_ERROR_TIP)
            # 清理 browser 对象
            BrowserController.close_browser()
            # 在这里处理无驱动打不开浏览器的情况
            self.__show_download_view()
        self.__auto_show_main_view()

    def __show_message(self, msg):
        self.ui.tip_label.setText(msg)

    def __show_download_view(self):
        DownloadViewSingleton.instance().show()
        self.__show_message(DRIVER_DOWNLOAD_FINISH_TIP)

    def __show_main_view(self):
        try:
            MainViewSingleton.instance().show()
            # AboutViewSingle.instance().show()
            self.hide()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __auto_show_main_view(self):
        if self._browser_is_open_bool and self._excel_path_is_select_bool:
            self.__show_main_view()

    def __show_advance(self):
        if self.ui.checkBox.isChecked():
            self.ui.btn_change_path.setVisible(True)
            self.ui.tip_label.setText(ADVANCE_TIP)
            self.ui.label_ecjtu_info.setVisible(False)
            self.ui.label_curr_chrome_path.setText(PATH_SELECT_TIP)
            self.ui.label_curr_chrome_path.setVisible(True)
        else:
            self.ui.btn_change_path.setVisible(False)
            self.ui.label_curr_chrome_path.setVisible(False)
            self.ui.label_ecjtu_info.setVisible(True)
            self.ui.tip_label.setText(NULL_STR)

    def __chang_path(self):
        try:
            excel_dir_path = QFileDialog.getExistingDirectory(self, PATH_DIALOG_INFO, "C:\\")
            if excel_dir_path is not None or excel_dir_path != "":
                SettingsInfo.BROWSER_EXE_PATH = excel_dir_path
        except BaseException:
            self.ui.tip_label.setText(ERROR_PATH_TIP)

    def set_tip_info(self, msg):
        """ 外界调用控制 label提示 """
        self.ui.tip_label.setText(msg)

    def set_path_info(self, msg):
        self.ui.label_curr_chrome_path(msg)
