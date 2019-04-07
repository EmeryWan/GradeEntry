import sys

from PyQt5.QtWidgets import QApplication

from zhang.BrowserOperate import BrowserOperate
from zhang.ExcelOperate import ExcelOperator
from zhang.MainWindow import Window
from zhang.Settings import SettingsInfo

if __name__ == '__main__':
    # 读取全部的配置文件
    setting = SettingsInfo()

    # 一定要从main传入　会奔溃
    excel_operator = ExcelOperator()
    browser_operator = BrowserOperate()

    app = QApplication(sys.argv)
    window = Window(excel_operator)
    window.show()
    sys.exit(app.exec_())
