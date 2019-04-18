import configparser
import cv2
import os

from GradeEntry.Log import LoggerSingleton


class SettingsInfo:
    EXCEL_FILES_PATH = os.path.join(os.getcwd(), "excel")

    WEBSITE = 'http://jwxt.ecjtu.jx.cn'

    HOMEPAGE = 'http://www.ecjtu.jx.cn'

    USER_ID = None

    PASSWORD = None

    BROWSER_NAME = 'chrome'

    BROWSER_EXE_PATH = None

    DRIVER_PATH = os.path.join(os.getcwd(), "config", "chromedriver.exe")

    # numpy
    ECJTU_LOGO = None

    # numpy
    ECJTU_LOGO_SMALL = None

    def __init__(self):
        try:
            self.__config_path = os.path.join(os.getcwd(), "config", 'settings.ini')
        except:
            self.__config_path = None

        if self.__config_path is not None:
            self.read_info()

        self.__read_logo()

    def read_info(self):

        ini_config = configparser.ConfigParser()
        ini_config.read(self.__config_path, encoding='utf-8')

        _excel_files_path = ini_config.get('excel', 'path')

        _website = ini_config.get('web', 'website')

        _homepage = ini_config.get('web', 'homepage')

        _user_id = ini_config.get('login', 'user')

        _password = ini_config.get('login', 'password')

        _browser_name = ini_config.get('browser', 'browser_name')

        _browser_exe_path = ini_config.get('browser', 'browser_exe_path')

        _driver_path = ini_config.get('browser', 'driver_path')

        if _excel_files_path != '' and _excel_files_path is not None:
            SettingsInfo.EXCEL_FILES_PATH = _excel_files_path
            SettingsInfo.EXCEL_FILES_PATH = str(SettingsInfo.EXCEL_FILES_PATH).strip()
            LoggerSingleton.instance().info("SettingsInfo->EXCEL_FILES_PATH " + str(SettingsInfo.EXCEL_FILES_PATH))

        if _website != '' and _website is not None:
            SettingsInfo.WEBSITE = _website
            SettingsInfo.WEBSITE = str(SettingsInfo.WEBSITE).strip()
            LoggerSingleton.instance().info("SettingsInfo->WEBSITE " + str(SettingsInfo.WEBSITE))

        if _homepage != '' and _homepage is not None:
            SettingsInfo.HOMEPAGE = _homepage
            SettingsInfo.HOMEPAGE = str(SettingsInfo.HOMEPAGE).strip()
            LoggerSingleton.instance().info("SettingsInfo->HOMEPAGE " + str(SettingsInfo.HOMEPAGE))

        if _user_id != '' and _user_id is not None:
            SettingsInfo.USER_ID = _user_id
            SettingsInfo.USER_ID = str(SettingsInfo.USER_ID).strip()
            LoggerSingleton.instance().info("SettingsInfo->USER_ID " + str(SettingsInfo.USER_ID))

        if _password != '' and _password is not None:
            SettingsInfo.PASSWORD = _password
            SettingsInfo.PASSWORD = str(SettingsInfo.PASSWORD).strip()

        if _browser_name != '' and _browser_name is not None:
            SettingsInfo.BROWSER_NAME = _browser_name
            SettingsInfo.BROWSER_NAME = str(SettingsInfo.BROWSER_NAME).strip()
            LoggerSingleton.instance().info("SettingsInfo->BROWSER_NAME " + str(SettingsInfo.BROWSER_NAME))

        if _browser_exe_path != '' and _browser_exe_path is not None:
            SettingsInfo.BROWSER_EXE_PATH = _browser_exe_path
            SettingsInfo.BROWSER_EXE_PATH = str(SettingsInfo.BROWSER_EXE_PATH).strip()
            LoggerSingleton.instance().info("SettingsInfo->BROWSER_EXE_PATH " + str(SettingsInfo.BROWSER_EXE_PATH))

        if _driver_path != '' and _driver_path is not None:
            SettingsInfo.DRIVER_PATH = _driver_path
            SettingsInfo.DRIVER_PATH = str(SettingsInfo.DRIVER_PATH).strip()
            LoggerSingleton.instance().info("SettingsInfo->DRIVER_PATH " + str(SettingsInfo.DRIVER_PATH))

    def __read_logo(self):
        try:
            path = os.path.join(os.getcwd(), "config", "ecjtu_logo.png")
            img = cv2.imread(path, flags=cv2.IMREAD_UNCHANGED)
            img_rgb = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2RGB)
            logo = cv2.resize(img_rgb, (81, 81), interpolation=cv2.INTER_CUBIC)
            SettingsInfo.ECJTU_LOGO = logo
        except:
            SettingsInfo.ECJTU_LOGO = None
            LoggerSingleton.instance().error('SettingsInfo->__read_logo 没有Logo')

    @classmethod
    def set_excel_file_path(cls, path):
        if path is not None and "" != path:
            SettingsInfo.EXCEL_FILES_PATH = path
