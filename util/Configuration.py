import configparser
import os

from util.Log import LoggerSingleton

# log 模板
LOG_ERROR_TEMPLATE = "%s --- %s --- ERROR"
LOG_INFO_TEMP = "%s -- %s -- %s -- INFO"
# LoggerSingleton.instance().error(LOG_ERROR_TEMPLATE % (self.__class__.__name__, Tool.get_current_fun_name()))
# LoggerSingleton.instance().info(LOG_INFO_TEMP % (self.__class__.__name__, Tool.get_current_fun_name(), ...))

# 配置文件目录
CONFIG_DIR_PATH = os.path.join(os.getcwd(), "config")

# VersionLad.py
CHROME_INSTALL_PATH = "C:\\Program Files (x86)\\Google\\Chrome\\Application"

CHROMEDRIVER_VERSION_JSON_NAME = "chromedriver.json"
CHROMEDRIVER_VERSION_JSON_PATH = os.path.join(CONFIG_DIR_PATH, CHROMEDRIVER_VERSION_JSON_NAME)

CHROMEDRIVER_SPIDER_JSON_NAME = "chromedriver_spider.json"
CHROMEDRIVER_SPIDER_JSON_PATH = os.path.join(CONFIG_DIR_PATH, CHROMEDRIVER_SPIDER_JSON_NAME)

CHROMEDRIVER_ZIP_NAME = "chromedriver_win32.zip"
CHROMEDRIVER_ZIP_PATH = os.path.join(CONFIG_DIR_PATH, CHROMEDRIVER_ZIP_NAME)

CHROMEDRIVER_NAME = "chromedriver.exe"
CHROMEDRIVER_PATH = os.path.join(CONFIG_DIR_PATH, CHROMEDRIVER_NAME)

# download
NPM_MIRRORS_URL = "https://npm.taobao.org/mirrors/chromedriver"

# MainView
ECJTU_MAIN_LOGO_PATH = os.path.join(CONFIG_DIR_PATH, "ecjtu_logo.png")
ECJTU_ICON_LOGO_PATH = os.path.join(CONFIG_DIR_PATH, "ecjtu_icon_logo.png")

# 录入界面表格上级 div 类名
CURRENT_PAGE_LEVEL_SELECT_ID = "stype"

MAIN_TABLE_PARENT_DIV_CLASS = "data-tab"

TAG_TABLE = "table"
TAG_TR = "tr"
TAG_INPUT = "input"
TAG_OPTION = "option"
TAG_SELECT = "select"

ATTRIBUTE_TYPE = "type"
ATTRIBUTE_VALUE = "value"
ATTRIBUTE_TEXT_TYPE = "text"
ATTRIBUTE_CHECKBOX_TYPE = "checkbox"

# BrowserController
LOGIN_FORM_ID = "login-action"
USER_INPUT_ID = "inputUser"
PASSWORD_INPUT_ID = "inputPassword"

# 一些标志
HUNDRED_DOUBLE_INPUT_BOOL = False
# DownLoad
DOWNLOAD_ERROR_SIGN = False
UNZIP_ERROR_SIGN = False


class SettingsInfo:
    USER_ID = None

    PASSWORD = None

    WEBSITE = "https://jwxt.ecjtu.edu.cn/"

    EXCEL_FILES_PATH = os.path.join(os.getcwd(), "excel")

    BROWSER_EXE_PATH = None

    # 该条不能更改 因重构保留
    HOMEPAGE = "https://jwxt.ecjtu.edu.cn/"

    # 该条不能更改 因重构保留
    DRIVER_PATH = os.path.join(os.getcwd(), "config", "chromedriver.exe")

    def __init__(self):
        try:
            self.__config_path = os.path.join(os.getcwd(), "config", "settings.ini")
        except BaseException:
            self.__config_path = None

        if self.__config_path is not None:
            self.read_info()

    def read_info(self):

        ini_config = configparser.ConfigParser()
        ini_config.read(self.__config_path, encoding="utf-8")

        _user_id = ini_config.get("login", "user")

        _password = ini_config.get("login", "password")

        _excel_files_path = ini_config.get("excel", "path")

        _website = ini_config.get("web", "website")

        _browser_exe_path = ini_config.get("browser", "browser_exe_path")

        if _excel_files_path != "" and _excel_files_path is not None:
            SettingsInfo.EXCEL_FILES_PATH = _excel_files_path
            SettingsInfo.EXCEL_FILES_PATH = str(SettingsInfo.EXCEL_FILES_PATH).strip()
            LoggerSingleton.instance().info("SettingsInfo -> EXCEL_FILES_PATH " + str(SettingsInfo.EXCEL_FILES_PATH))

        if _user_id != "" and _user_id is not None:
            SettingsInfo.USER_ID = _user_id
            SettingsInfo.USER_ID = str(SettingsInfo.USER_ID).strip()
            LoggerSingleton.instance().info("SettingsInfo -> USER_ID " + str(SettingsInfo.USER_ID))

        if _password != "" and _password is not None:
            SettingsInfo.PASSWORD = _password
            SettingsInfo.PASSWORD = str(SettingsInfo.PASSWORD).strip()

        if _website != "" and _website is not None:
            SettingsInfo.WEBSITE = _website
            SettingsInfo.WEBSITE = str(SettingsInfo.WEBSITE).strip()
            LoggerSingleton.instance().info("SettingsInfo -> WEBSITE " + str(SettingsInfo.WEBSITE))

        if _browser_exe_path != "" and _browser_exe_path is not None:
            SettingsInfo.BROWSER_EXE_PATH = _browser_exe_path
            SettingsInfo.BROWSER_EXE_PATH = str(SettingsInfo.BROWSER_EXE_PATH).strip()
            LoggerSingleton.instance().info("SettingsInfo -> BROWSER_EXE_PATH " + str(SettingsInfo.BROWSER_EXE_PATH))
