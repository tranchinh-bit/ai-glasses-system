from loguru import logger
import sys
import os

def setup_logging(log_file: str = "data/logs/core.log") -> None:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger.remove()
    logger.add(sys.stdout, level="INFO")
    logger.add(log_file, rotation="1 MB", retention=5, level="DEBUG")
