from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox

from ui.MapWindow import Ui_MapDialog
from util import Configuration, Tool
from util.Configuration import LOG_ERROR_TEMPLATE, ECJTU_ICON_LOGO_PATH
from util.LevelSystem import FIVE_LEVEL_MAP, TWO_LEVEL_MAP, FiveLevelSystemEnum, LevelSystemEnum, TwoLevelSystemEnum
from util.Log import LoggerSingleton

# final
#########################
MESSAGE_BOX_TITLE_WARNING = "警告"
MESSAGE_BOX_TITLE_SUCCESS = "成功"
MESSAGE_BOX_TITLE_ERROR = "错误"

MESSAGE_BOX_INFO_WARING = "请不要包含相同项目"
MESSAGE_BOX_INFO_SUCCESS = "更改成功"
MESSAGE_BOX_INFO_ERROR = "映射异常！ 请重试"


#########################

class MapView(QDialog):

    def __init__(self):
        super(MapView, self).__init__()
        self.ui = Ui_MapDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.__init_now_map_data()
        self.__show_icon()

        self.ui.btn_five.clicked.connect(self.__show_five_map)
        self.ui.btn_two.clicked.connect(self.__show_two_map)
        self.ui.btn_hundred.clicked.connect(self.__show_hundred)

        self.ui.btn_five_confirm.clicked.connect(self.__change_five_map)
        self.ui.btn_two_confirm.clicked.connect(self.__change_two_map)
        self.ui.btn_hundred_confirm.clicked.connect(self.__change_hundred_map)

        # 默认显示五级制
        self.ui.groupBox_hundred.setVisible(False)
        self.ui.groupBox_two.setVisible(False)

    def __show_icon(self):
        try:
            self.setWindowIcon(QIcon(ECJTU_ICON_LOGO_PATH))
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))

    def __show_five_map(self):
        self.ui.groupBox_five.setVisible(True)
        self.ui.groupBox_two.setVisible(False)
        self.ui.groupBox_hundred.setVisible(False)

    def __show_two_map(self):
        self.ui.groupBox_five.setVisible(False)
        self.ui.groupBox_two.setVisible(True)
        self.ui.groupBox_hundred.setVisible(False)

    def __show_hundred(self):
        self.ui.groupBox_five.setVisible(False)
        self.ui.groupBox_two.setVisible(False)
        self.ui.groupBox_hundred.setVisible(True)

    def __init_five_map(self):
        self.ui.five_now_you.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.YOU_XIU.value))
        self.ui.five_now_liang.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.LIANG_HAO.value))
        self.ui.five_now_zhong.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.ZHONG_DENG.value))
        self.ui.five_now_jige.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.JI_GE.value))
        self.ui.five_now_bujige.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.BU_JI_GE.value))
        self.ui.five_now_mianxiu.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.MIAN_XIU.value))
        self.ui.five_now_huankao.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.HUAN_KAO.value))
        self.ui.five_now_quekao.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.QUE_KAO.value))
        self.ui.five_now_quxiaozige.setText(FIVE_LEVEL_MAP.get(FiveLevelSystemEnum.QU_XIAO_ZI_GE.value))

    def __init_two_map(self):
        self.ui.two_now_hege.setText(TWO_LEVEL_MAP.get(TwoLevelSystemEnum.HE_GE.value))
        self.ui.two_now_buhege.setText(TWO_LEVEL_MAP.get(TwoLevelSystemEnum.BU_HE_GE.value))
        self.ui.two_now_mianxiu.setText(TWO_LEVEL_MAP.get(TwoLevelSystemEnum.MIAN_XIU.value))
        self.ui.two_now_huankao.setText(TWO_LEVEL_MAP.get(TwoLevelSystemEnum.HUAN_KAO.value))
        self.ui.two_now_quekao.setText(TWO_LEVEL_MAP.get(TwoLevelSystemEnum.QUE_KAO.value))
        self.ui.two_now_quxiaozige.setText(TWO_LEVEL_MAP.get(TwoLevelSystemEnum.QU_XIAO_ZI_GE.value))

    def __init_hundred(self):
        if Configuration.HUNDRED_DOUBLE_INPUT_BOOL:
            self.ui.hundred_double_checkBox.setChecked(True)

    def __change_five_map(self):

        try:
            if not self.__repeat_judge(LevelSystemEnum.FIVE):
                QMessageBox.question(self, MESSAGE_BOX_TITLE_WARNING, MESSAGE_BOX_INFO_WARING, QMessageBox.Yes,
                                     QMessageBox.Yes)
                return

            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.YOU_XIU.value,
                               self.ui.five_edit_you.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.LIANG_HAO.value,
                               self.ui.five_edit_liang.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.ZHONG_DENG.value,
                               self.ui.five_edit_zhong.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.JI_GE.value,
                               self.ui.five_edit_jige.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.BU_JI_GE.value,
                               self.ui.five_edit_bujige.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.MIAN_XIU.value,
                               self.ui.five_edit_mianxiu.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.HUAN_KAO.value,
                               self.ui.five_edit_huankao.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.QUE_KAO.value,
                               self.ui.five_edit_quekao.text().strip())
            self.__set_new_map(LevelSystemEnum.FIVE, FiveLevelSystemEnum.QU_XIAO_ZI_GE.value,
                               self.ui.five_edit_quxiaozige.text().strip())

            self.__init_five_map()
            self.__reset_edit(LevelSystemEnum.FIVE)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            QMessageBox.question(self, MESSAGE_BOX_INFO_ERROR, MESSAGE_BOX_TITLE_ERROR, QMessageBox.Yes,
                                 QMessageBox.Yes)

    def __change_two_map(self):

        try:
            if not self.__repeat_judge(LevelSystemEnum.TWO):
                QMessageBox.question(self, MESSAGE_BOX_TITLE_WARNING, MESSAGE_BOX_INFO_WARING, QMessageBox.Yes,
                                     QMessageBox.Yes)
                return

            self.__set_new_map(LevelSystemEnum.TWO, TwoLevelSystemEnum.HE_GE.value,
                               self.ui.two_edit_hege.text().strip())
            self.__set_new_map(LevelSystemEnum.TWO, TwoLevelSystemEnum.BU_HE_GE.value,
                               self.ui.two_edit_buhege.text().strip())
            self.__set_new_map(LevelSystemEnum.TWO, TwoLevelSystemEnum.MIAN_XIU.value,
                               self.ui.two_edit_mianxiu.text().strip())
            self.__set_new_map(LevelSystemEnum.TWO, TwoLevelSystemEnum.HUAN_KAO.value,
                               self.ui.two_edit_huankao.text().strip())
            self.__set_new_map(LevelSystemEnum.TWO, TwoLevelSystemEnum.QUE_KAO.value,
                               self.ui.two_edit_quekao.text().strip())
            self.__set_new_map(LevelSystemEnum.TWO, TwoLevelSystemEnum.QU_XIAO_ZI_GE.value,
                               self.ui.two_edit_quxiaozige.text().strip())

            self.__init_two_map()
            self.__reset_edit(LevelSystemEnum.TWO)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
            QMessageBox.question(self, MESSAGE_BOX_INFO_ERROR, MESSAGE_BOX_TITLE_ERROR, QMessageBox.Yes,
                                 QMessageBox.Yes)

    def __change_hundred_map(self):
        if self.ui.hundred_double_checkBox.isChecked():
            sign = True
        else:
            sign = False
        Configuration.HUNDRED_DOUBLE_INPUT_BOOL = sign

        self.__init_hundred()
        QMessageBox.information(self, MESSAGE_BOX_TITLE_SUCCESS, MESSAGE_BOX_INFO_SUCCESS, QMessageBox.Yes,
                                QMessageBox.Yes)

    def __init_now_map_data(self):
        self.__init_five_map()
        self.__init_two_map()
        self.__init_hundred()

    def __set_new_map(self, sign, k, v):
        if v is None or v == "":
            return
        if sign == LevelSystemEnum.FIVE:
            FIVE_LEVEL_MAP[k] = v
        if sign == LevelSystemEnum.TWO:
            TWO_LEVEL_MAP[k] = v

    def __repeat_judge(self, sign):
        # 判断是否有过该元素
        if sign == LevelSystemEnum.FIVE:
            values = FIVE_LEVEL_MAP.values()
            edit_list = self.ui.groupBox_five.findChildren(QLineEdit)
        else:
            values = TWO_LEVEL_MAP.values()
            edit_list = self.ui.groupBox_two.findChildren(QLineEdit)

        # 去除为空的情况
        count = 0
        text_set = set()

        for edit in edit_list:
            temp = edit.text().strip()
            if temp in values:
                return False
            if temp != "":
                text_set.add(temp)
                count += 1
        if len(text_set) != count:
            return False
        return True

    def __reset_edit(self, sign):
        if sign == LevelSystemEnum.FIVE:
            edit_list = self.ui.groupBox_five.findChildren(QLineEdit)
            for edit in edit_list:
                edit.clear()
        if sign == LevelSystemEnum.TWO:
            edit_list = self.ui.groupBox_two.findChildren(QLineEdit)
            for edit in edit_list:
                edit.clear()
