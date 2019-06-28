from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from singleton.AboutViewSingleton import AboutViewSingle
from ui.DownloadWindow import Ui_DownloadDialog
from util import Tool
from util.Configuration import LOG_ERROR_TEMPLATE, LOG_INFO_TEMP, DOWNLOAD_ERROR_SIGN, UNZIP_ERROR_SIGN, \
    ECJTU_ICON_LOGO_PATH
from util.Log import LoggerSingleton
from util.VersionLoad import DownLoad, Version

#########################
# final

VERSION_INFO_TEMPLATE = "Chrome version: %s  -  Driver version: %s"

DOWNLOAD_SUCCESS_MSG = "下载完成"
DOWNLOAD_ERROR_MSG = "错误！ 下载失败，请检查网络"
UNZIP_SUCCESS_MSG = "解压完成 已完成所有步骤"
UNZIP_ERROR_MSG = "错误！ 解压失败"


#########################

class DownloadChromedriveThread(QThread):
    single_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(DownloadChromedriveThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        DownLoad.start_download()
        if DOWNLOAD_ERROR_SIGN:
            self.single_out.emit(False)
        else:
            self.single_out.emit(True)


class UnzipFileThread(QThread):
    single_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(UnzipFileThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        DownLoad.unzip()
        if UNZIP_ERROR_SIGN:
            self.single_out.emit(False)
        else:
            self.single_out.emit(True)


#########################

class DownloadView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DownloadDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # 初始化控件
        self.ui.label_down.setVisible(False)
        self.ui.label_unzip.setVisible(False)
        self.ui.progressBar.setValue(0)

        self.__show_icon()

        # 初始化线程
        self.__download_thread = DownloadChromedriveThread()
        self.__unzip_thread = UnzipFileThread()
        self.__download_thread.single_out.connect(self.__download_signal)
        self.__unzip_thread.single_out.connect(self.__unzip_signal)

        # 完成信号
        self.__complete_download = False
        self.__complete_unzip = False

        # 开始处理
        self.__process_all()

    #########################

    def __show_icon(self):
        try:
            self.setWindowIcon(QIcon(ECJTU_ICON_LOGO_PATH))
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __process_all(self):
        self.__process_version()
        self.__process_download()

    def __process_version(self):
        try:
            Version.get_version_info()
            msg = VERSION_INFO_TEMPLATE % (Version.CHROME_VERSION, Version.CHROMEDRIVER_NEED_VERSION)
            # msg = "Chrome:" + Version.CHROME_VERSION + ",  Driver" + Version.CHROMEDRIER_NEED_VERSION
            LoggerSingleton.instance().info(
                LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), msg))
            self.__show_version_info(msg)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __process_download(self):
        try:
            self.__start_download_thread()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __process_unzip(self):
        try:
            self.__start_unzip_thread()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __show_version_info(self, msg):
        self.ui.label_version.setText(msg)
        self.ui.progressBar.setValue(30)
        self.ui.label_down.setVisible(True)

    def __show_download_info(self, msg):
        if msg is not None:
            self.ui.label_down.setText(msg)
        self.ui.progressBar.setValue(70)
        self.ui.label_unzip.setVisible(True)

    def __show_unzip_info(self, msg):
        self.ui.label_unzip.setText(msg)
        self.ui.progressBar.setValue(100)

    def __start_download_thread(self):
        try:
            if not self.__download_thread.isRunning():
                self.__download_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __start_unzip_thread(self):
        try:
            if not self.__unzip_thread.isRunning():
                self.__unzip_thread.start()
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __download_signal(self, signal):
        if signal:
            self.__show_download_info(DOWNLOAD_SUCCESS_MSG)
            # 下载完成后再开始解压线程
            self.__complete_download = True
            self.__process_unzip()
        else:
            self.__show_download_info(DOWNLOAD_ERROR_MSG)
            # 显示信息界面
            self.__show_error_view()

    def __unzip_signal(self, signal):
        if signal:
            self.__show_unzip_info(UNZIP_SUCCESS_MSG)
            self.__complete_unzip = True
            # 完成所有步骤 关闭当前界面
            self.__close_download_view()
        else:
            self.__show_unzip_info(UNZIP_ERROR_MSG)
            # 显示信息界面
            self.__show_error_view()

    def __close_download_view(self):
        if self.__complete_download and self.__complete_unzip:
            self.close()

    def __show_error_view(self):
        AboutViewSingle.instance().show()
        AboutViewSingle.instance().show_error()
