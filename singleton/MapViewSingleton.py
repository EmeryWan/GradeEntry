import threading

from view.MapView import MapView


class MapViewSingleton:
    _instance_lock = threading.Lock()
    __map_view_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if MapViewSingleton.__map_view_instance is None:
            with MapViewSingleton._instance_lock:
                if MapViewSingleton.__map_view_instance is None:
                    MapViewSingleton.__map_view_instance = MapView()
        return MapViewSingleton.__map_view_instance
