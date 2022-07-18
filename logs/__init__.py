""" 
Logger Utility
"""
import logging
import os
import sys


def get_logger(name: str) -> logging.Logger:
    """Get logger template for the given name.

    Args:
        name (str): file name

    Returns:
        logging.Logger: logger instance
    """
    logger = logging.getLogger(name)
    logger.handlers = []
    handler = logging.StreamHandler(sys.stdout)

    level = logging.getLevelName(os.getenv("LOGGING_LEVEL", "INFO"))
    logger.setLevel(level)

    format_logger = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - " + " - %(message)s"
    )

    handler.setFormatter(format_logger)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
