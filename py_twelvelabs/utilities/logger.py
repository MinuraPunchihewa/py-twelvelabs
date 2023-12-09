import os
import logging
from logging.config import dictConfig


class ColorFormatter(logging.Formatter):
    """
    A logging formatter that adds color to the log output.
    """

    green = "\x1b[32;20m"
    default = "\x1b[39;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(processName)15s %(levelname)-8s %(name)s: %(message)s"

    FORMATS = {
        logging.DEBUG: logging.Formatter(green + format + reset),
        logging.INFO: logging.Formatter(default + format + reset),
        logging.WARNING: logging.Formatter(yellow + format + reset),
        logging.ERROR: logging.Formatter(red + format + reset),
        logging.CRITICAL: logging.Formatter(bold_red + format + reset),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        return log_fmt.format(record)


def configure_logging():
    """
    Configure logging.

    The log level can be set by setting the environment variable PY_TWELVE_LABS_LOG_LEVEL.
    """

    log_level = os.environ.get("PY_TWELVE_LABS_LOG_LEVEL", None)
    if log_level is not None:
        log_level = getattr(logging, log_level)
    else:
        log_level = logging.INFO

    logging_config = dict(
        version=1,
        formatters={"f": {"()": ColorFormatter}},
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "f",
            }
        },
        loggers={
            "": {
                "handlers": ["console"],
                "level": logging.WARNING,
            },
            "__main__": {
                "level": log_level,
            }
        },
    )
    dictConfig(logging_config)


def get_logger(name=None):
    """
    Get a logger instance.

    :param name: Name of the logger. If None, the root logger is returned.
    :return: Logger instance.
    """
    configure_logging()

    return logging.getLogger(name)
