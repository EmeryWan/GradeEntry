# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(781, 442)
        AboutDialog.setMinimumSize(QtCore.QSize(781, 442))
        AboutDialog.setMaximumSize(QtCore.QSize(781, 442))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        AboutDialog.setFont(font)
        self.label_logo = QtWidgets.QLabel(AboutDialog)
        self.label_logo.setGeometry(QtCore.QRect(160, 30, 81, 81))
        self.label_logo.setMinimumSize(QtCore.QSize(81, 81))
        self.label_logo.setMaximumSize(QtCore.QSize(81, 81))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_logo.setFont(font)
        self.label_logo.setObjectName("label_logo")
        self.label_2 = QtWidgets.QLabel(AboutDialog)
        self.label_2.setGeometry(QtCore.QRect(310, 50, 331, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AboutDialog)
        self.label_3.setGeometry(QtCore.QRect(160, 230, 231, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_11 = QtWidgets.QLabel(AboutDialog)
        self.label_11.setGeometry(QtCore.QRect(310, 110, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(AboutDialog)
        self.label_12.setGeometry(QtCore.QRect(310, 160, 71, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_error = QtWidgets.QLabel(AboutDialog)
        self.label_error.setGeometry(QtCore.QRect(30, 60, 72, 331))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_error.setFont(font)
        self.label_error.setObjectName("label_error")
        self.layoutWidget = QtWidgets.QWidget(AboutDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 300, 449, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(111, 41))
        self.label_8.setMaximumSize(QtCore.QSize(111, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(151, 41))
        self.label_6.setMaximumSize(QtCore.QSize(151, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setMinimumSize(QtCore.QSize(171, 41))
        self.label_9.setMaximumSize(QtCore.QSize(171, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(151, 41))
        self.label_5.setMaximumSize(QtCore.QSize(151, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        self.label_10.setMinimumSize(QtCore.QSize(171, 41))
        self.label_10.setMaximumSize(QtCore.QSize(171, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(410, 110, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(AboutDialog)
        self.label_4.setGeometry(QtCore.QRect(410, 160, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Dialog"))
        self.label_logo.setText(_translate("AboutDialog", "logo"))
        self.label_2.setText(_translate("AboutDialog", "华东交通大学 - 软件学院 - 和平研究院"))
        self.label_3.setText(_translate("AboutDialog", "问题反馈："))
        self.label_11.setText(_translate("AboutDialog", "github"))
        self.label_12.setText(_translate("AboutDialog", "码云"))
        self.label_error.setText(_translate("AboutDialog", "错\n"
"误\n"
"界\n"
"面"))
        self.label_8.setText(_translate("AboutDialog", "QQ："))
        self.label_6.setText(_translate("AboutDialog", "23683340"))
        self.label_9.setText(_translate("AboutDialog", "张薇老师"))
        self.label_5.setText(_translate("AboutDialog", "767571431"))
        self.label_10.setText(_translate("AboutDialog", "万义晨"))
        self.label.setText(_translate("AboutDialog", "https://github.com/EmeryWan/GradeEntry"))
        self.label_4.setText(_translate("AboutDialog", "https://gitee.com/EmeryWan/GradeEntry"))
