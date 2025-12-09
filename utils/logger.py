import logging
from logging import Logger


def get_logger(name: str) -> Logger:
    """Return a configured logger with a simple console handler.

    Usage:
        logger = get_logger(__name__)
        logger.info("message")
    """

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
