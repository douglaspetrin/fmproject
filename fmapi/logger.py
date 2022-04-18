import logging
from datetime import datetime


class Logger:

    _module_name = None
    _instance = None

    def __init__(self, log_name="log_name"):
        self.log_level = "DEBUG"
        self.log_name = log_name
        self.is_file_handler = False

    @classmethod
    def get_logger(cls, log_name="log_name", is_file_handler=False):
        if cls._instance is None:
            cls._instance = cls(log_name)
            cls._instance.is_file_handler = is_file_handler
        return cls._instance._get_logger()

    def _get_file_handler(self, formatter):

        log_file_name = f"{datetime.now().date()}.log"
        file_handler = logging.FileHandler(filename=f"{log_file_name}")
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)

        return file_handler

    def _get_logger(self):

        logger = logging.getLogger(name=self.log_name)
        logger.setLevel(self.log_level)

        formatter = logging.Formatter(f"%(asctime)s::%(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        if self.is_file_handler:
            file_handler = self._get_file_handler(formatter)
            logger.handlers = [file_handler, stream_handler]
        else:
            logger.handlers = [stream_handler]

        logger.propagate = False

        return logger
