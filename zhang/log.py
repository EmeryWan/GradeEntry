import logging
import os
import time


class Logger:
    def __init__(self, logger_name='log_default_name'):

        if not os.path.exists(r".//config//logs_file"):
            os.makedirs(".//config//logs_file")

        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_name = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime())
        self.log_file_path = r".//config//logs_file" + self.log_file_path + r'.log'
        self.file_output_level = 'DEBUG'
        self.console_output_level = 'DEBUG'
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):

        if not self.logger.handlers:
            # 控制台
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 文件
            file_handler = logging.FileHandler(self.log_file_path, mode='w', encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)

        return self.logger


logger = Logger().get_logger()
