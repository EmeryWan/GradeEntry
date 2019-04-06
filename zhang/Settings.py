import configparser
import os


class SettingsInfo:

    EXCEL_FILES_PATH = os.path.join(os.getcwd(), "..", "excel")

    WEBSITE = 'http://jwxt.ecjtu.jx.cn'

    USER_ID = None

    PASSWORD = None

    def __init__(self):
        try:
            self.__config_path = os.path.join(os.getcwd(), "..", "config", 'settings.ini')
        except:
            self.__config_path = None

        if self.__config_path is not None:
            self.read_info()

    def read_info(self):

        ini_config = configparser.ConfigParser()
        ini_config.read(self.__config_path, encoding='utf-8')

        # print(ini_config.sections())

        _excel_files_path = ini_config.get('excel', 'path')
        # print(_excel_files_path)

        _website = ini_config.get('web', 'website')
        # print(_website)

        _user_id = ini_config.get('login', 'user')
        # print(_user_id)

        _password = ini_config.get('login', 'password')
        # print(_password)

        if _excel_files_path != '' and _excel_files_path is not None:
            SettingsInfo.EXCEL_FILES_PATH = _excel_files_path
            # print(SettingsInfo.EXCEL_FILES_PATH)

        if _website != '' and _website is not None:
            SettingsInfo.WEBSITE = _website
            # print(SettingsInfo.WEBSITE)

        if _user_id != '' and _user_id is not None:
            SettingsInfo.USER_ID = _user_id
            # print(SettingsInfo.USER_ID)

        if _password != '' and _password is not None:
            SettingsInfo.PASSWORD = _password
            # print(SettingsInfo.PASSWORD)
