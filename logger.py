from sys import stdout
from loguru import logger

config = {
    "handlers": [
        {
            "sink": stdout,
            "format": '<green>{time:DD-MM-YYYY HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>',
            "colorize": True
        },
    ],
}

logger.configure(**config)
