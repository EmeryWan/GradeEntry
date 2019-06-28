# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DownloadWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        DownloadDialog.setObjectName("DownloadDialog")
        DownloadDialog.resize(541, 341)
        DownloadDialog.setMinimumSize(QtCore.QSize(541, 341))
        DownloadDialog.setMaximumSize(QtCore.QSize(541, 341))
        self.label_version = QtWidgets.QLabel(DownloadDialog)
        self.label_version.setGeometry(QtCore.QRect(30, 20, 481, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_version.setFont(font)
        self.label_version.setObjectName("label_version")
        self.label_down = QtWidgets.QLabel(DownloadDialog)
        self.label_down.setGeometry(QtCore.QRect(30, 80, 481, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_down.setFont(font)
        self.label_down.setObjectName("label_down")
        self.label_info = QtWidgets.QLabel(DownloadDialog)
        self.label_info.setGeometry(QtCore.QRect(30, 270, 481, 61))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_info.setFont(font)
        self.label_info.setObjectName("label_info")
        self.label_unzip = QtWidgets.QLabel(DownloadDialog)
        self.label_unzip.setGeometry(QtCore.QRect(30, 140, 481, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_unzip.setFont(font)
        self.label_unzip.setObjectName("label_unzip")
        self.progressBar = QtWidgets.QProgressBar(DownloadDialog)
        self.progressBar.setGeometry(QtCore.QRect(70, 220, 391, 23))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(DownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDialog)

    def retranslateUi(self, DownloadDialog):
        _translate = QtCore.QCoreApplication.translate
        DownloadDialog.setWindowTitle(_translate("DownloadDialog", "正在尝试下载驱动"))
        self.label_version.setText(_translate("DownloadDialog", "请稍等，正在读取系统信息 ... ... "))
        self.label_down.setText(_translate("DownloadDialog", "请稍等，正在下载驱动 ... ..."))
        self.label_info.setText(_translate("DownloadDialog", "信息：\n"
"该程序不会在电脑上安装任何软件，清理删除文件夹即可"))
        self.label_unzip.setText(_translate("DownloadDialog", "请稍等，正在解压 ... ..."))

