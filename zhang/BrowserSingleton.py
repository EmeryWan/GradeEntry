import threading
from selenium import webdriver
from zhang import log

logger = log.logger
logger.name = 'Browser Singleton'


class BrowserSingleton:
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
                        driver_path = r"..//config//chromedriver.exe"
                        option = webdriver.ChromeOptions()
                        option.add_argument('disable-infobars')
                        BrowserSingleton.__browser_instance = webdriver.Chrome(executable_path=driver_path,
                                                                               options=option)
                    except:
                        logger.error('！！！无法获得浏览器')
                        # BrowserSingleton.__browser_instance = None
        return BrowserSingleton.__browser_instance

    @classmethod
    def close_instance(cls):
        if BrowserSingleton.__browser_instance is not None:
            with BrowserSingleton._instance_lock:
                if BrowserSingleton.__browser_instance is not None:
                    try:
                        BrowserSingleton.instance().close()
                    except:
                        pass
