import logging


class DebugInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG or record.levelno == logging.INFO


class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING