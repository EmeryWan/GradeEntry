import sys

from PyQt5.QtWidgets import QApplication

from zhang.BrowserOperate import Browser
from zhang.ExcelOperate import Excel
from zhang.MainWindow import Window
from zhang.Settings import SettingsInfo

if __name__ == '__main__':
    # 读取全部的配置文件
    setting = SettingsInfo()

    # 一定要从main传入　会奔溃
    excel = Excel()
    browser = Browser()

    app = QApplication(sys.argv)
    window = Window(browser, excel)
    window.show()
    sys.exit(app.exec_())
