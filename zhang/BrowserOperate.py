from zhang.BrowserSingleton import BrowserSingleton


class Browser:

    def __init__(self):
        self.browser_singleton = BrowserSingleton()
        self.browser = self.browser_singleton.get_browser()
        self.browser.get('http://jwxt.ecjtu.jx.cn')

    def find_from(self):
        pass


if __name__ == '__main__':
    b = Browser()
