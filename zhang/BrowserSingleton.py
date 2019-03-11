from selenium import webdriver


class BrowserSingleton:
    brow = None

    def __int__(self):
        self.brow = None

    def get_browser(self):
        if self.brow is None:
            try:
                path = r"..//config//chromedriver"

                option = webdriver.ChromeOptions()
                option.add_argument('disable-infobars')
                self.brow = webdriver.Chrome(executable_path=path, options=option)
            except:
                print("得不到浏览器")
                return None
        return self.brow

    def close_browser(self):
        pass


# if __name__ == "__main__":
#     b = BrowserSingleton()
#     b.get_browser()
