import sys
import time

from PyQt5.QtWidgets import QApplication

from zhang.BrowserOperate import BrowserOperate
from zhang.ExcelOperate import ExcelOperator
from zhang.MainWindow import Window
from zhang.Settings import SettingsInfo

if __name__ == '__main__':
    setting = SettingsInfo()

    browser_operator = BrowserOperate()
    time.sleep(0.2)
    excel_operator = ExcelOperator()

    app = QApplication(sys.argv)
    window = Window(excel_operator)
    window.show()

    sys.exit(app.exec_())
