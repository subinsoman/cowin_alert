import logging
from logging import config as logging_config


class SixdeeLogger:
    sixdeelogger = None

    def __init__(self):
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - [%(module)s:%(levelname)s] - %(message)s"
                },
                "root": {
                    "format": "ROOT - %(asctime)s - [%(module)s:%(levelname)s] - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default"
                },
                "root_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "root"
                }
            },
            "loggers": {
                "app": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    # Don't send it up my namespace for additional handling
                    "propagate": False
                }
            },
            "root": {
                "handlers": ["root_console"],
                "level": "DEBUG"
            }
        }
        logging_config.dictConfig(LOGGING_CONFIG)

    def getlogger(self, name):
        return logging.getLogger(name)
