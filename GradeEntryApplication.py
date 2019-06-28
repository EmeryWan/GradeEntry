import sys
from PyQt5.QtWidgets import QApplication

from singleton.AboutViewSingleton import AboutViewSingle
from singleton.InitViewSingleton import InitViewSingleton
from util.Configuration import SettingsInfo

if __name__ == '__main__':

    try:
        SettingsInfo()

        app = QApplication(sys.argv)

        init_view = InitViewSingleton.instance()
        init_view.show()

        sys.exit(app.exec_())

    except BaseException:
        app = QApplication(sys.argv)

        error_view = AboutViewSingle.instance()
        error_view.show()
        error_view.show_error()

        sys.exit(app.exec_())
