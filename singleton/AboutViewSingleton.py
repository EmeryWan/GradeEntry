import threading

from view.AboutView import AboutView


class AboutViewSingle:
    _instance_lock = threading.Lock()
    __about_view_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if AboutViewSingle.__about_view_instance is None:
            with AboutViewSingle._instance_lock:
                if AboutViewSingle.__about_view_instance is None:
                    AboutViewSingle.__about_view_instance = AboutView()
        return AboutViewSingle.__about_view_instance