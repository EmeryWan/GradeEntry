from selenium import webdriver

path = r"..//configure//chromedriver"

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
driver = webdriver.Chrome(executable_path=path, options=option)
