from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog

from ui.AboutWindow import Ui_AboutDialog
from util.Configuration import ECJTU_MAIN_LOGO_PATH


class AboutView(QDialog):
    def __init__(self):
        super(AboutView, self).__init__()
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.ui.label_error.setVisible(False)

        self.__init_icon()

    def __init_icon(self):
        self.ui.label_logo.setPixmap(QPixmap(ECJTU_MAIN_LOGO_PATH))
        self.ui.label_logo.setScaledContents(True)
        self.setWindowIcon(QIcon(ECJTU_MAIN_LOGO_PATH))

    def show_error(self):
        """ 错误页面显示 """
        self.ui.label_error.setVisible(True)
