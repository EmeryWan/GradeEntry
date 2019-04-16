import time

from zhang.BrowserSingleton import BrowserSingleton

b = BrowserSingleton.instance()
print(BrowserSingleton.instance())

time.sleep(5)
BrowserSingleton.close_instance()

time.sleep(5)
print(BrowserSingleton.instance())

