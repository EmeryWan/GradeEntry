import sys
import time

from PyQt5.QtWidgets import QApplication

from GradeEntry.BrowserOperate import BrowserOperate
from GradeEntry.ExcelOperate import ExcelOperator
from GradeEntry.MainWindow import Window
from GradeEntry.Settings import SettingsInfo

if __name__ == '__main__':
    # 读取配置文件 进行默认配置
    setting = SettingsInfo()

    # 打开浏览器
    browser_operator = BrowserOperate()
    time.sleep(0.2)

    # Excel初始化操作
    excel_operator = ExcelOperator()

    # 窗体
    app = QApplication(sys.argv)
    window = Window(excel_operator)
    window.show()

    sys.exit(app.exec_())
