import json
import os
import time
import zipfile

import requests
from bs4 import BeautifulSoup

from singleton.AboutViewSingleton import AboutViewSingle
from util import Tool, Configuration
from util.Configuration import CONFIG_DIR_PATH, CHROMEDRIVER_ZIP_NAME, CHROMEDRIVER_VERSION_JSON_PATH, \
    CHROME_INSTALL_PATH, CHROMEDRIVER_ZIP_PATH, CHROMEDRIVER_NAME, NPM_MIRRORS_URL, CHROMEDRIVER_PATH, \
    LOG_ERROR_TEMPLATE, LOG_INFO_TEMP, CHROMEDRIVER_SPIDER_JSON_PATH, SettingsInfo, CHROME_INSTALL_PATH_USER
from util.Log import LoggerSingleton

# Version final
DRIVER_VERSION_DIVISION = 73

SPLIT_VERSION_INFO_SIGN = "."

CHROME_EXE = "chrome.exe"

VERSION_CONFIG_MAP = {

}

VERSION_SPIDER_MAP = {

}

# Spider final

TAOBAO_NPM_PAGE_CONTAINER_CLASS = ".container"
TAOBAO_NPM_PAGE_LIST_TAG = "pre"
TAOBAO_NPM_PAGE_LIST_INFO_TAG = "a"

NEW_VERSION = 73


########################

class Version:
    CHROME_VERSION = ''

    CHROMEDRIVER_NEED_VERSION = ''

    chrome_path = ''

    def __init__(self):
        pass

    @classmethod
    def confirm_chrome_default_path(cls):
        try:
            # 系统安装目录
            try:
                admin_path = CHROME_INSTALL_PATH
                admin_list = os.listdir(admin_path)
                if CHROME_EXE in admin_list:
                    cls.chrome_path = admin_path
                    LoggerSingleton.instance().info(
                        LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), admin_path))
                    return admin_path
            except BaseException:
                # FileNotFindException
                pass

            # 用户安装目录
            try:
                user_path = CHROME_INSTALL_PATH_USER
                user_list = os.listdir(user_path)
                if CHROME_EXE in user_list:
                    cls.chrome_path = user_path
                    LoggerSingleton.instance().info(
                        LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), user_path))
                    return user_path
            except BaseException:
                pass

            return cls.chrome_path

        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
            Tool.show_error_page()
            return ""

    @classmethod
    def get_version_info(cls):
        # 读取本地 chrome 版本
        cls.__load_chrome_version()
        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), cls.CHROME_VERSION))
        # 查询版本
        cls.__load_driver_version()
        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), cls.CHROMEDRIVER_NEED_VERSION))

    @classmethod
    def __load_chrome_version(cls):
        try:
            if SettingsInfo.BROWSER_EXE_PATH is not None:
                LoggerSingleton.instance().info(
                    LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(SettingsInfo.BROWSER_EXE_PATH)))
                path = SettingsInfo.BROWSER_EXE_PATH
            else:
                path = cls.confirm_chrome_default_path()

            if path is None or path == "":
                Tool.show_error_page()
                return

            dir_names = os.listdir(path)
            for name in dir_names:
                if name[0].isdigit():
                    LoggerSingleton.instance().info(
                        LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), str(name)))
                    Version.CHROME_VERSION = name.split(SPLIT_VERSION_INFO_SIGN)[0]
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
            Tool.show_error_page()

    @classmethod
    def __load_driver_version(cls):
        if Version.CHROME_VERSION == '':
            Tool.show_error_page()
            return
        if int(Version.CHROME_VERSION) < DRIVER_VERSION_DIVISION:
            # 旧式命名版本
            cls.process_old_driver_map()
        elif int(Version.CHROME_VERSION) >= DRIVER_VERSION_DIVISION:
            # 新式命名版本
            cls.__process_new_driver_map()
        else:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
            Tool.show_error_page()

    @classmethod
    def process_old_driver_map(cls):
        try:
            # 读取本地文件json
            with open(CHROMEDRIVER_VERSION_JSON_PATH, "r") as f:
                global VERSION_CONFIG_MAP
                VERSION_CONFIG_MAP = json.load(f)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
            Tool.show_error_page()
            return
            # 配置
        Version.CHROMEDRIVER_NEED_VERSION = VERSION_CONFIG_MAP.get(Version.CHROME_VERSION)

    @classmethod
    def __process_new_driver_map(cls):
        # 进行爬虫 会覆盖本地文件
        InfoSpider.start_spider()
        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), VERSION_SPIDER_MAP))
        Version.CHROMEDRIVER_NEED_VERSION = VERSION_SPIDER_MAP.get(Version.CHROME_VERSION)


class DownLoad:

    def __init__(self):
        pass

    @classmethod
    def start_download(cls):

        if Version.CHROMEDRIVER_NEED_VERSION == '' or Version.CHROMEDRIVER_NEED_VERSION is None:
            return False

        url = NPM_MIRRORS_URL + "/" + Version.CHROMEDRIVER_NEED_VERSION + "/" + CHROMEDRIVER_ZIP_NAME

        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), url))

        try:
            cls.__down(url)
        except BaseException:
            try:
                cls.__down(url)
            except BaseException:
                cls.__delete_exist()
                Configuration.DOWNLOAD_ERROR_SIGN = True
                LoggerSingleton.instance().error(
                    LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
                Tool.show_error_page()

        return True

    @classmethod
    def __down(cls, url):
        # 删除存在文件
        cls.__delete_exist()
        # 进行下载
        r = requests.get(url)
        with open(CHROMEDRIVER_ZIP_PATH, "wb") as f:
            f.write(r.content)

    @classmethod
    def unzip(cls):

        names = os.listdir(CONFIG_DIR_PATH)
        if CHROMEDRIVER_ZIP_NAME not in names:
            return False

        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), CHROMEDRIVER_ZIP_PATH))

        try:
            z = zipfile.is_zipfile(CHROMEDRIVER_ZIP_PATH)
            if z:
                zf = zipfile.ZipFile(CHROMEDRIVER_ZIP_PATH, "r")
                if CHROMEDRIVER_NAME in zf.namelist():
                    zf.extract(CHROMEDRIVER_NAME, CONFIG_DIR_PATH)
        except BaseException:
            Configuration.UNZIP_ERROR_SIGN = True
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))
        return True

    @classmethod
    def __delete_exist(cls):
        """ 清除 config 文件夹中旧版 chromedriver """
        names = os.listdir(CONFIG_DIR_PATH)

        LoggerSingleton.instance().info(
            LOG_INFO_TEMP % (cls.__class__.__name__, Tool.get_current_fun_name(), names))

        try:
            if CHROMEDRIVER_ZIP_NAME in names:
                os.remove(CHROMEDRIVER_ZIP_PATH)

            if CHROMEDRIVER_NAME in names:
                os.remove(CHROMEDRIVER_PATH)
        except BaseException:
            LoggerSingleton.instance().error(
                LOG_ERROR_TEMPLATE % (cls.__class__.__name__, Tool.get_current_fun_name()))


class InfoSpider:
    spider_map = {

    }

    def __init__(self):
        pass

    @classmethod
    def start_spider(cls):
        cls.__do_spider()
        global VERSION_SPIDER_MAP
        VERSION_SPIDER_MAP = cls.spider_map
        cls.__save_spider_info()

    @classmethod
    def __do_spider(cls):
        # 尝试2次
        try:
            cls.__spider()
        except BaseException:
            time.sleep(2)
            try:
                cls.__spider()
            except BaseException:
                AboutViewSingle.instance().show()
                AboutViewSingle.instance().show_error()

    @classmethod
    def __spider(cls):
        mirrors_page = requests.get(NPM_MIRRORS_URL)
        soup = BeautifulSoup(mirrors_page.content, "html.parser")
        page_tag_pre = soup.select_one(TAOBAO_NPM_PAGE_CONTAINER_CLASS).select_one(TAOBAO_NPM_PAGE_LIST_TAG)
        page_tag_a = page_tag_pre.select(TAOBAO_NPM_PAGE_LIST_INFO_TAG)

        cls.spider_map.clear()

        # 获取数据
        for a in page_tag_a:
            # 去除最后的 /
            info = str(a.string).strip()[:-1]
            version = info.split(SPLIT_VERSION_INFO_SIGN)[0]
            if version.isdigit():
                # 只爬取版本号 >= 73
                if int(version) >= NEW_VERSION:
                    # {str -> str}  相同版本号获取最后一个
                    cls.spider_map[version] = info

    @classmethod
    def __save_spider_info(cls):
        with open(CHROMEDRIVER_SPIDER_JSON_PATH, "w") as f:
            json.dump(cls.spider_map, f)
