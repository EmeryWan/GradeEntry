import threading
from view.DownloadView import DownloadView


class DownloadViewSingleton:
    _instance_lock = threading.Lock()
    __download_view_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if DownloadViewSingleton.__download_view_instance is None:
            with DownloadViewSingleton._instance_lock:
                if DownloadViewSingleton.__download_view_instance is None:
                    DownloadViewSingleton.__download_view_instance = DownloadView()
        return DownloadViewSingleton.__download_view_instance
