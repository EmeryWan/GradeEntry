import logging
import os
import threading
import time

"""
    控制台输出级别为info
    文件输出级别 debug
"""


class LoggerSingleton:
    _instance_lock = threading.Lock()
    __logger_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if LoggerSingleton.__logger_instance is None:
            with LoggerSingleton._instance_lock:
                if LoggerSingleton.__logger_instance is None:
                    LoggerSingleton.__logger_instance = Logger().get_logger()
        return LoggerSingleton.__logger_instance


class Logger:
    __log_file_dir = os.path.join(os.getcwd(), "..", "config", "logs_file")

    def __init__(self, logger_name='log_default_name'):

        # self.__log_file_dir = os.path.join(os.getcwd(), "..", "config", "logs_file")

        if not os.path.exists(self.__log_file_dir):
            os.makedirs(self.__log_file_dir)

        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_time = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime())
        self.log_file_name = "成绩录入软件日志" + self.log_file_time
        # self.log_file_path = self.__log_file_dir + "//" + self.log_file_name + r'.log'
        self.log_file_path = os.path.join(Logger.__log_file_dir, (self.log_file_name + r'.log'))
        # print(self.log_file_path)
        self.file_output_level = 'WARNING'
        self.console_output_level = 'DEBUG'
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def get_logger(self):
        """
        这个方法在其他地方请不要调用
        写日志请使用 LoggerSingleton.instance
        """
        if not self.logger.handlers:
            # 控制台
            # console_handler = logging.StreamHandler()
            # console_handler.setFormatter(self.formatter)
            # console_handler.setLevel(self.console_output_level)
            # self.logger.addHandler(console_handler)

            # 文件
            file_handler = logging.FileHandler(self.log_file_path, mode='w', encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)

        return self.logger

    @classmethod
    def clean_log_file(cls):
        try:
            log_file_list = os.listdir(cls.__log_file_dir)
            for log_file in log_file_list:
                file_real_path = os.path.join(cls.__log_file_dir, log_file)
                if os.path.isfile(file_real_path):
                    os.remove(file_real_path)
        except:
            pass

