import threading
from selenium import webdriver
from GradeEntry.Log import LoggerSingleton
from GradeEntry.Settings import SettingsInfo


class BrowserSingleton:
    __browser_name = SettingsInfo.BROWSER_NAME
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
                    try:

                        if cls.__browser_name == 'chrome':
                            LoggerSingleton.instance().info("BrowserSingleton -> chrome")
                            driver_path = cls.__driver_path
                            options = webdriver.ChromeOptions()
                            options.add_argument('disable-infobars')
                            if cls.__browser_exe_path is not None and cls.__browser_exe_path != '':
                                # 指定浏览器exe位置
                                options.binary_location = cls.__browser_exe_path
                                BrowserSingleton.__browser_instance = webdriver.Chrome(executable_path=driver_path,
                                                                                       options=options)
                            else:
                                # 默认不指定
                                BrowserSingleton.__browser_instance = webdriver.Chrome(executable_path=driver_path,
                                                                                       options=options)

                        elif cls.__browser_name == 'firefox':
                            LoggerSingleton.instance().info("BrowserSingleton -> firefox")
                            driver_path = cls.__driver_path
                            options = webdriver.FirefoxOptions()
                            if cls.__browser_exe_path is not None and cls.__browser_exe_path != '':
                                options.binary_location = cls.__browser_exe_path
                                BrowserSingleton.__browser_instance = webdriver.Firefox(executable_path=driver_path,
                                                                                        options=options)
                            else:
                                BrowserSingleton.__browser_instance = webdriver.Firefox(executable_path=driver_path)
                        else:
                            LoggerSingleton.instance().info("BrowserSingleton -> 默认 注意！可能配置有问题")
                            # 默认为 chrome
                            driver_path = cls.__driver_path
                            options = webdriver.ChromeOptions()
                            options.add_argument('disable-infobars')
                            BrowserSingleton.__browser_instance = webdriver.Chrome(executable_path=driver_path,
                                                                                   options=options)


                    except:
                        LoggerSingleton.instance().error("无法获得浏览器实例！请检查配置")
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
                        except:
                            BrowserSingleton.__browser_instance = None
                    except:
                        LoggerSingleton.instance().error("无法关闭浏览器实例！")
