import threading

from view.InitView import InitView


class InitViewSingleton:
    _instance_lock = threading.Lock()
    __init_view_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if InitViewSingleton.__init_view_instance is None:
            with InitViewSingleton._instance_lock:
                if InitViewSingleton.__init_view_instance is None:
                    InitViewSingleton.__init_view_instance = InitView()
        return InitViewSingleton.__init_view_instance
