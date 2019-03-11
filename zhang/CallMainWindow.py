import sys

from PyQt5.QtWidgets import QApplication

from zhang.MainWindow import Window

if __name__ == '__main__':

    # 读取全部的配置文件

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
