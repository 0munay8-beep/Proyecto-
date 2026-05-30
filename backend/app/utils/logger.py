"""
Logging configuration
"""

import logging
from app.config import get_settings

settings = get_settings()


def get_logger(name: str) -> logging.Logger:
    """Get configured logger"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger