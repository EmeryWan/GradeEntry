# import threading
#
# from zhang.browser import browser
#
#
# def synchronized(func):
#     func.__lock__ = threading.Lock()
#
#     def lock_func(*args, **kwargs):
#         with func.__lock__:
#             return func(*args, **kwargs)
#
#     return lock_func
#
#
# class Singleton(browser):
#     _instance = None
#
#     @synchronized
#     def __new__(cls, *args, **kwargs):
#         if Singleton._instance is None:
#             cls._instance = super().__new__(cls)
#         return cls._instance
