# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EntryWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(501, 651)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_advance = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_advance.setGeometry(QtCore.QRect(10, 530, 481, 81))
        self.groupBox_advance.setMouseTracking(False)
        self.groupBox_advance.setObjectName("groupBox_advance")
        self.btn_click_checkbox = QtWidgets.QPushButton(self.groupBox_advance)
        self.btn_click_checkbox.setGeometry(QtCore.QRect(10, 30, 451, 41))
        self.btn_click_checkbox.setMinimumSize(QtCore.QSize(221, 29))
        self.btn_click_checkbox.setObjectName("btn_click_checkbox")
        self.checkBox_advance = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_advance.setGeometry(QtCore.QRect(10, 500, 91, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_advance.sizePolicy().hasHeightForWidth())
        self.checkBox_advance.setSizePolicy(sizePolicy)
        self.checkBox_advance.setMinimumSize(QtCore.QSize(91, 27))
        self.checkBox_advance.setMaximumSize(QtCore.QSize(91, 27))
        self.checkBox_advance.setChecked(False)
        self.checkBox_advance.setObjectName("checkBox_advance")
        self.groupBox_excel_file = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_excel_file.setGeometry(QtCore.QRect(10, 40, 481, 351))
        self.groupBox_excel_file.setObjectName("groupBox_excel_file")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_excel_file)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 462, 149))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 12, 1, 1, 1)
        self.btn_select_excel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_select_excel.setMinimumSize(QtCore.QSize(80, 29))
        self.btn_select_excel.setMaximumSize(QtCore.QSize(80, 29))
        self.btn_select_excel.setObjectName("btn_select_excel")
        self.gridLayout_2.addWidget(self.btn_select_excel, 9, 1, 1, 1)
        self.btn_re_view_excel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_re_view_excel.setMinimumSize(QtCore.QSize(80, 29))
        self.btn_re_view_excel.setMaximumSize(QtCore.QSize(80, 29))
        self.btn_re_view_excel.setObjectName("btn_re_view_excel")
        self.gridLayout_2.addWidget(self.btn_re_view_excel, 11, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(77, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 8, 1, 1, 1)
        self.listWidget_excel_list = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget_excel_list.setMinimumSize(QtCore.QSize(373, 140))
        self.listWidget_excel_list.setMaximumSize(QtCore.QSize(373, 140))
        self.listWidget_excel_list.setObjectName("listWidget_excel_list")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_excel_list.addItem(item)
        self.gridLayout_2.addWidget(self.listWidget_excel_list, 7, 0, 7, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 10, 1, 1, 1)
        self.groupBox_excel_info = QtWidgets.QGroupBox(self.groupBox_excel_file)
        self.groupBox_excel_info.setGeometry(QtCore.QRect(10, 200, 461, 141))
        self.groupBox_excel_info.setObjectName("groupBox_excel_info")
        self.widget = QtWidgets.QWidget(self.groupBox_excel_info)
        self.widget.setGeometry(QtCore.QRect(50, 30, 363, 96))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_excel_sheet = QtWidgets.QComboBox(self.widget)
        self.comboBox_excel_sheet.setMinimumSize(QtCore.QSize(361, 31))
        self.comboBox_excel_sheet.setMaximumSize(QtCore.QSize(361, 31))
        self.comboBox_excel_sheet.setObjectName("comboBox_excel_sheet")
        self.comboBox_excel_sheet.addItem("")
        self.gridLayout.addWidget(self.comboBox_excel_sheet, 0, 0, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(358, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 2)
        self.comboBox_get_row = QtWidgets.QComboBox(self.widget)
        self.comboBox_get_row.setMinimumSize(QtCore.QSize(161, 31))
        self.comboBox_get_row.setMaximumSize(QtCore.QSize(161, 31))
        self.comboBox_get_row.setObjectName("comboBox_get_row")
        self.comboBox_get_row.addItem("")
        self.gridLayout.addWidget(self.comboBox_get_row, 2, 0, 1, 1)
        self.comboBox_get_col = QtWidgets.QComboBox(self.widget)
        self.comboBox_get_col.setMinimumSize(QtCore.QSize(161, 31))
        self.comboBox_get_col.setMaximumSize(QtCore.QSize(161, 31))
        self.comboBox_get_col.setObjectName("comboBox_get_col")
        self.comboBox_get_col.addItem("")
        self.gridLayout.addWidget(self.comboBox_get_col, 2, 1, 1, 1)
        self.label_top_info = QtWidgets.QLabel(self.centralwidget)
        self.label_top_info.setGeometry(QtCore.QRect(11, 11, 511, 21))
        self.label_top_info.setMinimumSize(QtCore.QSize(511, 21))
        self.label_top_info.setMaximumSize(QtCore.QSize(511, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_top_info.setFont(font)
        self.label_top_info.setObjectName("label_top_info")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(20, 440, 461, 41))
        self.btn_start.setMinimumSize(QtCore.QSize(231, 29))
        self.btn_start.setObjectName("btn_start")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 400, 399, 21))
        self.label_2.setMinimumSize(QtCore.QSize(388, 21))
        self.label_2.setMaximumSize(QtCore.QSize(428, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_advance.setTitle(_translate("MainWindow", "高级"))
        self.btn_click_checkbox.setText(_translate("MainWindow", "点击页面中的所有CheckBox"))
        self.checkBox_advance.setText(_translate("MainWindow", "高级选项"))
        self.groupBox_excel_file.setTitle(_translate("MainWindow", "请选择需要的 Excel 文件"))
        self.btn_select_excel.setText(_translate("MainWindow", "选择"))
        self.btn_re_view_excel.setText(_translate("MainWindow", "刷新"))
        self.listWidget_excel_list.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.listWidget_excel_list.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        __sortingEnabled = self.listWidget_excel_list.isSortingEnabled()
        self.listWidget_excel_list.setSortingEnabled(False)
        item = self.listWidget_excel_list.item(0)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(1)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(2)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(3)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(4)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(5)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(6)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(7)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(8)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_excel_list.item(9)
        item.setText(_translate("MainWindow", "新建项目"))
        self.listWidget_excel_list.setSortingEnabled(__sortingEnabled)
        self.groupBox_excel_info.setTitle(_translate("MainWindow", "Excel 读取内容设置"))
        self.comboBox_excel_sheet.setItemText(0, _translate("MainWindow", "请选择Sheet"))
        self.comboBox_get_row.setItemText(0, _translate("MainWindow", "行"))
        self.comboBox_get_col.setItemText(0, _translate("MainWindow", "列"))
        self.label_top_info.setText(_translate("MainWindow", "软件关闭后浏览器也会同关闭，如需要浏览器请不要关闭此程序"))
        self.btn_start.setText(_translate("MainWindow", "开始录入"))
        self.label_2.setText(_translate("MainWindow", "请到需要录成绩的页面再点击开始按钮"))

