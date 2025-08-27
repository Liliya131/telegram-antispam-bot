import logging

class Logger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def info(self, msg: str):
        self._logger.info(msg)

    def error(self, msg: str):
        self._logger.error(msg)

    def debug(self, msg: str):
        self._logger.debug(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def critical(self, msg: str):
        self._logger.critical(msg)
