import threading

from view.MainView import MainView


class MainViewSingleton:
    _instance_lock = threading.Lock()
    __main_view_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if MainViewSingleton.__main_view_instance is None:
            with MainViewSingleton._instance_lock:
                if MainViewSingleton.__main_view_instance is None:
                    MainViewSingleton.__main_view_instance = MainView()
        return MainViewSingleton.__main_view_instance
