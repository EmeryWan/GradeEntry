import os
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QPushButton

from zhang.BrowserOperate import BrowserOperate
from zhang.EntryWindow import Ui_MainWindow
from zhang.Log import LoggerSingleton, Logger
from zhang.Settings import SettingsInfo


class ReOpenBrowserThread(QThread):
    def __init__(self, parent=None):
        super(ReOpenBrowserThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        BrowserOperate.close_browser()
        time.sleep(0.2)
        BrowserOperate.open_website()


class BrowserFromEntryThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None, grade_list=None):
        super(BrowserFromEntryThread, self).__init__(parent)
        self.grade_list = grade_list

    def __del__(self):
        self.wait()

    def set_grade_list(self, grade_list):
        self.grade_list = grade_list

    def run(self):
        sign = BrowserOperate.start_entry_data(grade_list=self.grade_list)
        self.signal_out.emit(sign)


class CheckboxThread(QThread):
    signal_out = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(CheckboxThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        sign = BrowserOperate.click_all_checkbox()
        self.signal_out.emit(sign)


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
        self.re_open_browser_thread = ReOpenBrowserThread()
        self.browser_entry_thread.signal_out.connect(self.thread_page_not_find_signal)
        self.check_box_thread.signal_out.connect(self.thread_page_not_find_signal)

        # 数据暂存
        self.request_excel_object = None
        self.request_excel_sheet_name = None

    def thread_page_not_find_signal(self, sign):
        if not sign:
            QMessageBox.warning(self, '警告', '请到正确的操作页面！', QMessageBox.Yes, QMessageBox.Yes)

    def window_init(self):
        try:
            # 控件的可见性 可用性
            self.ui.groupBox_advance.setVisible(False)
            # self.ui.btn_start.setEnabled(False)
            # self.ui.btn_click_checkbox.setEnabled(False)

            # 控件的绑定和初始化
            self.ui.checkBox_advance.stateChanged.connect(self.set_advance_visible)
            self.ui.btn_re_view_excel.clicked.connect(self.fill_excel_listWidget)
            self.ui.btn_open_dir.clicked.connect(self.set_my_excel_dir)
            self.ui.btn_select_excel.clicked.connect(self.fill_sheet_comboBox)
            self.ui.comboBox_excel_sheet.currentTextChanged.connect(self.fill_row_col_info)  # combobox 当前选择改变时执行
            self.ui.btn_start.clicked.connect(self.start_entry)
            self.ui.btn_click_checkbox.clicked.connect(self.check_box)
            self.ui.commandLinkButton_feedback.clicked.connect(self.feedback)
            self.ui.btn_re_open_browser.clicked.connect(self.re_open_browser)
            self.ui.btn_clean_log.clicked.connect(self.clean_log_file)

            self.load_ecjtu_logo()
        except:
            LoggerSingleton.instance().error("Window->window_init 内部错误")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', '注意！关闭程序后浏览器也会关闭！', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 关闭浏览器
            BrowserOperate.close_browser()
            event.accept()
        else:
            event.ignore()

    def load_ecjtu_logo(self):
        try:
            img = SettingsInfo.ECJTU_LOGO
            if img is not None:
                height, width, channel = img.shape
                bytesPerLine = 3 * width
                # temp = QImage(img, width, height, bytesPerLine, QImage.Format_ARGB32)
                temp = QImage(img, height, width, bytesPerLine, QImage.Format_RGB888)
                logo = QPixmap.fromImage(temp)
                self.ui.ecjtu_logo_label.setScaledContents(True)
                # logo = QtGui.QPixmap(img).scaled(self.ui.ecjtu_logo_label.width(), self.ui.ecjtu_logo_label.height())
                self.ui.ecjtu_logo_label.setPixmap(logo)
        except:
            LoggerSingleton.instance().error("Window->load_ecjtu_logo 内部错误")

    def set_advance_visible(self):
        if self.ui.checkBox_advance.isChecked():
            self.ui.groupBox_advance.setVisible(True)
            self.ui.groupBox_about_info.setVisible(False)
        else:
            self.ui.groupBox_advance.setVisible(False)
            self.ui.groupBox_about_info.setVisible(True)

    def set_my_excel_dir(self):
        try:
            current_path = os.getcwd()
            excel_dir_path = QFileDialog.getExistingDirectory(self, '请选取文件夹', current_path)
            if excel_dir_path is not None and "" != excel_dir_path:
                SettingsInfo.set_excel_file_path(excel_dir_path)
                self.ui.listWidget_excel_list.clear()
                self.fill_excel_listWidget()
        except:
            LoggerSingleton.instance().error("Window->set_my_excel_dir 内部错误")

    def fill_excel_listWidget(self):
        try:
            excel_list = self.excel_operate.get_all_excel_name_lists()
            if excel_list is None:
                QMessageBox.question(self, '问题', '不能读取该路径下的文件', QMessageBox.Yes, QMessageBox.Yes)
                self.ui.listWidget_excel_list.clear()
            elif len(excel_list) == 0:
                self.set_my_excel_dir()
                excel_list = self.excel_operate.get_all_excel_name_lists()
                # QMessageBox.warning(self, '没有文件', '没有读取到Excel文件\n请再确认一下', QMessageBox.Yes, QMessageBox.Yes)
            if excel_list is not None and len(excel_list) > 0:
                self.ui.listWidget_excel_list.clear()
                self.ui.listWidget_excel_list.addItems(excel_list)
        except:
            LoggerSingleton.instance().error("Window->fill_excel_listWidget 内部错误")

    def fill_sheet_comboBox(self):
        try:
            # 如果combobox 长度为0
            try:
                excel_item = self.ui.listWidget_excel_list.currentItem()
            except:
                QMessageBox.warning(self, '警告', '请先选择Excel文件！', QMessageBox.Yes | QMessageBox.Yes)
                excel_item = None

            if excel_item is not None:
                excel_name = str(excel_item.text()).strip()

                sign = self.excel_operate.get_all_info(excel_name)
                if sign:
                    self.request_excel_object = self.excel_operate.get_excel_object_info(excel_name)
                    sheet_list = self.request_excel_object.sheet_lists
                    if sheet_list is not None:
                        self.ui.comboBox_excel_sheet.clear()
                        self.ui.comboBox_excel_sheet.addItem('请选择Sheet')
                        self.ui.comboBox_excel_sheet.addItems(sheet_list)
                        self.ui.comboBox_get_row.clear()
                        self.ui.comboBox_get_row.addItem('先选择Sheet')
                        self.ui.comboBox_get_col.clear()
                        self.ui.comboBox_get_col.addItem('先选择Sheet')
                    else:
                        # QMessage
                        QMessageBox.warning(self, '错误', '程序无法填充Excel(sheet)信息', QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.warning(self, '无法读取', '文件被其他软件占用无法读取\n可能修改了未保存，请关闭Excel后再试一次', QMessageBox.Yes,
                                        QMessageBox.Yes)
        except:
            LoggerSingleton.instance().error("Window->fill_sheet_comboBox 内部错误")

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
                    # QMessageBox 无法读取行列信息
                    QMessageBox.warning(self, '错误', '程序无法填充Excel(行列)信息', QMessageBox.Yes, QMessageBox.Yes)
        except:
            LoggerSingleton.instance().warning("Window->fill_row_col_info 因为第一个是中文提示会报错 偶尔单次为正常现象 连续多次请注意")

    def get_grade_info_list(self):
        try:
            excel_name = self.request_excel_object.excel_name
            sheet_name = self.request_excel_sheet_name

            row = str(int(self.ui.comboBox_get_row.currentText()) - 1)
            col = str(int(colname_to_colnum(self.ui.comboBox_get_col.currentText())) - 1)

            grade_info_list = self.excel_operate.get_grade_info(excel_name, sheet_name, row, col)
            return grade_info_list
        except:
            LoggerSingleton.instance().error("Window->get_grade_info_list 内部错误 不再指定页面进行操作可能触发")
            return []

    def start_entry(self):
        try:
            reply = QMessageBox.question(self, '请确定', '请确定在录入成绩界面\n\n录入成绩会占用鼠标键盘事件\n完毕前请不要使用鼠标键盘\n使用鼠标键盘可能会造成某些无法录入\n\n程序不会进行姓名匹配，有错误重复操作一次即可',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 关闭浏览器
                try:
                    grade_info_list = self.get_grade_info_list()
                    if len(grade_info_list) > 0:
                        self.start_browser_entry_thread(grade_info_list)
                    else:
                        QMessageBox.warning(self, '错误', '程序无法成绩信息信息', QMessageBox.Yes, QMessageBox.Yes)
                except:
                    LoggerSingleton.instance().warning("Window->start_entry 有不当图像界面操作该信息为正常现象")
            else:
                pass
        except:
            LoggerSingleton.instance().error("Window->start_entry 内部错误")

    def check_box(self):
        # 添加一个判断是否在指定页面
        try:
            reply = QMessageBox.question(self, '请确定', '请确定在勾选界面\n\n录入成绩会占用鼠标键盘事件\n完毕前请不要使用鼠标键盘\n\n使用鼠标可能会造成某些无法勾选',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.start_check_box_thread()
                except:
                    # QMessageBox
                    LoggerSingleton.instance().warning("Window->check_box 有不当图像界面操作该信息为正常现象")
            else:
                pass
        except:
            LoggerSingleton.instance().error("Window->check_box 内部错误")

    def start_browser_entry_thread(self, grade_info_list):
        try:
            self.browser_entry_thread.set_grade_list(grade_info_list)
            self.browser_entry_thread.start()
        except:
            LoggerSingleton.instance().error("Window->start_browser_entry_thread 内部错误")
            QMessageBox.warning(self, '错误', '程序内部填充成绩线程错误！', QMessageBox.Yes, QMessageBox.Yes)

    def start_check_box_thread(self):
        try:
            self.check_box_thread.start()
        except:
            LoggerSingleton.instance().error("Window->start_check_box_thread 内部错误")
            QMessageBox.warning(self, '错误', '程序内部处理checkBox线程错误！', QMessageBox.Yes, QMessageBox.Yes)

    def start_re_browser_thread(self):
        try:
            self.re_open_browser_thread.run()
        except:
            LoggerSingleton.instance().error("Window->start_re_browser_thread 内部错误")
            QMessageBox.warning(self, '错误', '无法打开新的浏览器，请尝试重启程序', QMessageBox.Yes, QMessageBox.Yes)

    def feedback(self):
        about_title = "华东交通大学 软件学院\n和平研究院"
        about_text = "请将 config/logs 中的日志文件打包 说明一下错误场景或截图\n发送至 emerywan@gmail.com\n或联系QQ: 767571431"
        about_info = about_title + "\n\n" + about_text
        # QMessageBox.about(self, '联系', about_info)

        img = SettingsInfo.ECJTU_LOGO
        logo = None
        if img is not None:
            img = cv2.resize(img, (81, 81), interpolation=cv2.INTER_CUBIC)
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            # # img = QImage(img_rgb, width, height, bytesPerLine, QImage.Format_ARGB32)
            temp = QImage(img, height, width, bytesPerLine, QImage.Format_RGB888)
            logo = QPixmap.fromImage(temp)

        about = QMessageBox()
        about.setWindowTitle('联系')
        about.setText(about_info)
        if logo is not None:
            about.setIconPixmap(logo)
        about.addButton(QPushButton('确定'), QMessageBox.YesRole)
        about.exec_()

    def re_open_browser(self):
        try:
            reply = QMessageBox.question(self, '重启浏览器', '请确定浏览器被误关闭后再继续', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.start_re_browser_thread()
        except:
            LoggerSingleton.instance().error("Window->re_open_browser 内部错误")

    def clean_log_file(self):
        try:
            Logger.clean_log_file()
        except:
            LoggerSingleton.instance().error("Window->clean_log_file 内部错误")


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
