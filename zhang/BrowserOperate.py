from zhang.BrowserSingleton import BrowserSingleton


class Browser:

    def __init__(self):
        browser_singleton = BrowserSingleton()
        browser = browser_singleton.get_browser()
        browser.get('http://jwxt.ecjtu.jx.cn')
