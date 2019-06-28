import threading
from selenium import webdriver

from util.Configuration import SettingsInfo
from util.Log import LoggerSingleton


class BrowserSingleton:
    __browser_exe_path = SettingsInfo.BROWSER_EXE_PATH
    __driver_path = SettingsInfo.DRIVER_PATH

    _instance_lock = threading.Lock()
    __browser_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):

        if BrowserSingleton.__browser_instance is None:
            with BrowserSingleton._instance_lock:
                if BrowserSingleton.__browser_instance is None:

                    # 一些配置
                    driver_path = cls.__driver_path
                    options = webdriver.ChromeOptions()
                    options.add_argument('disable-infobars')

                    try:
                        if cls.__browser_exe_path is not None and cls.__browser_exe_path != '':
                            exe_path = cls.__browser_exe_path + "\\chrome.exe"
                            # 指定浏览器exe位置
                            options.binary_location = exe_path
                            BrowserSingleton.__browser_instance = webdriver.Chrome(executable_path=driver_path,
                                                                                   options=options)
                        else:
                            # 默认安装位置
                            BrowserSingleton.__browser_instance = webdriver.Chrome(executable_path=driver_path,
                                                                                   options=options)
                    except BaseException:
                        # 处理无驱动情况 交给 initView 处理
                        LoggerSingleton.instance().error("无法获得浏览器实例！请检查配置")
                        return None
        return BrowserSingleton.__browser_instance

    @classmethod
    def close_instance(cls):
        if BrowserSingleton.__browser_instance is not None:
            with BrowserSingleton._instance_lock:
                if BrowserSingleton.__browser_instance is not None:
                    try:
                        try:
                            BrowserSingleton.instance().close()
                            BrowserSingleton.__browser_instance = None
                        except BaseException:
                            BrowserSingleton.__browser_instance = None
                    except BaseException:
                        LoggerSingleton.instance().error("无法关闭浏览器实例！")
