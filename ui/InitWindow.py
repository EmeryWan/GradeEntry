# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InitWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InItDialog(object):
    def setupUi(self, InItDialog):
        InItDialog.setObjectName("InItDialog")
        InItDialog.resize(867, 499)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        InItDialog.setFont(font)
        InItDialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.init_label_info_1 = QtWidgets.QLabel(InItDialog)
        self.init_label_info_1.setGeometry(QtCore.QRect(310, 90, 431, 71))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.init_label_info_1.setFont(font)
        self.init_label_info_1.setObjectName("init_label_info_1")
        self.init_label_info_2 = QtWidgets.QLabel(InItDialog)
        self.init_label_info_2.setGeometry(QtCore.QRect(340, 40, 341, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.init_label_info_2.setFont(font)
        self.init_label_info_2.setObjectName("init_label_info_2")
        self.tip_label = QtWidgets.QLabel(InItDialog)
        self.tip_label.setGeometry(QtCore.QRect(70, 380, 721, 41))
        self.tip_label.setObjectName("tip_label")
        self.btn_show_main_window = QtWidgets.QPushButton(InItDialog)
        self.btn_show_main_window.setEnabled(False)
        self.btn_show_main_window.setGeometry(QtCore.QRect(540, 280, 161, 51))
        self.btn_show_main_window.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_show_main_window.setObjectName("btn_show_main_window")
        self.logo_label = QtWidgets.QLabel(InItDialog)
        self.logo_label.setGeometry(QtCore.QRect(150, 50, 81, 81))
        self.logo_label.setObjectName("logo_label")
        self.label_ecjtu_info = QtWidgets.QLabel(InItDialog)
        self.label_ecjtu_info.setGeometry(QtCore.QRect(240, 440, 361, 31))
        self.label_ecjtu_info.setObjectName("label_ecjtu_info")
        self.checkBox = QtWidgets.QCheckBox(InItDialog)
        self.checkBox.setGeometry(QtCore.QRect(180, 280, 151, 41))
        self.checkBox.setObjectName("checkBox")
        self.btn_change_path = QtWidgets.QPushButton(InItDialog)
        self.btn_change_path.setGeometry(QtCore.QRect(180, 340, 481, 31))
        self.btn_change_path.setObjectName("btn_change_path")
        self.label_curr_chrome_path = QtWidgets.QLabel(InItDialog)
        self.label_curr_chrome_path.setGeometry(QtCore.QRect(70, 440, 721, 31))
        self.label_curr_chrome_path.setObjectName("label_curr_chrome_path")
        self.btn_select_excel = QtWidgets.QPushButton(InItDialog)
        self.btn_select_excel.setGeometry(QtCore.QRect(540, 200, 161, 51))
        self.btn_select_excel.setMinimumSize(QtCore.QSize(161, 51))
        self.btn_select_excel.setMaximumSize(QtCore.QSize(161, 51))
        self.btn_select_excel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_select_excel.setObjectName("btn_select_excel")
        self.btn_open_browser = QtWidgets.QPushButton(InItDialog)
        self.btn_open_browser.setGeometry(QtCore.QRect(170, 200, 161, 51))
        self.btn_open_browser.setMinimumSize(QtCore.QSize(161, 51))
        self.btn_open_browser.setMaximumSize(QtCore.QSize(161, 51))
        self.btn_open_browser.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_open_browser.setObjectName("btn_open_browser")

        self.retranslateUi(InItDialog)
        QtCore.QMetaObject.connectSlotsByName(InItDialog)

    def retranslateUi(self, InItDialog):
        _translate = QtCore.QCoreApplication.translate
        InItDialog.setWindowTitle(_translate("InItDialog", "配置界面"))
        self.init_label_info_1.setText(_translate("InItDialog", "该程序只能控制浏览器最后打开的的一个窗口\n"
"请尽量保证只打开一个窗口"))
        self.init_label_info_2.setText(_translate("InItDialog", "注意："))
        self.tip_label.setText(_translate("InItDialog", "tip_info"))
        self.btn_show_main_window.setText(_translate("InItDialog", "主界面"))
        self.logo_label.setText(_translate("InItDialog", "logo"))
        self.label_ecjtu_info.setText(_translate("InItDialog", "华东交通大学 - 软件学院 - 和平研究院"))
        self.checkBox.setText(_translate("InItDialog", "高级"))
        self.btn_change_path.setText(_translate("InItDialog", "点击更改 Chrome 浏览器的安装位置"))
        self.label_curr_chrome_path.setText(_translate("InItDialog", "path_info"))
        self.btn_select_excel.setText(_translate("InItDialog", "选择文件夹"))
        self.btn_open_browser.setText(_translate("InItDialog", "打开浏览器"))

