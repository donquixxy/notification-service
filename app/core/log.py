import logging


def set_logger(level:str = "INFO"):
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "NOTSET": logging.NOTSET,
    }

    log_level = log_levels.get(level.upper(), logging.INFO)

    fmt = logging.Formatter("[%(levelname)s]-[%(asctime)s]-[%(filename)s:%(lineno)s]-%(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(fmt)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(handler)


set_logger()