import logging
import os
from datetime import datetime
from typing import Optional, Union

# Directory for log files
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Timestamped log filename
LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Default formatter used by handlers
_DEFAULT_FORMATTER = logging.Formatter(
    "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

# Helper to parse level argument (accepts int or string)
def _parse_level(level: Optional[Union[int, str]]) -> int:
    if level is None:
        # allow overriding via environment variable LOG_LEVEL (e.g. "DEBUG", "INFO")
        level_str = os.getenv("LOG_LEVEL", "INFO")
        try:
            return int(level_str)
        except (TypeError, ValueError):
            return getattr(logging, level_str.upper(), logging.INFO)
    if isinstance(level, int):
        return level
    return getattr(logging, str(level).upper(), logging.INFO)

def get_logger(name: Optional[str] = None, level: Optional[Union[int, str]] = None) -> logging.Logger:
    """
    Return a configured logger with both console and file handlers.

    - `name`: logger name (typically __name__ of the module).
    - `level`: logging level for console output (int or string). If None, uses LOG_LEVEL env var or INFO.

    Behavior:
    - FileHandler records all levels (DEBUG and above) into logs/<timestamp>.log
    - StreamHandler (console) uses the provided level
    - Avoids adding duplicate handlers if called multiple times for the same logger
    """
    resolved_level = _parse_level(level)

    logger = logging.getLogger(name)
    # make logger permissive; handlers will filter appropriately
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # File handler: keep all messages (DEBUG+)
        fh = logging.FileHandler(LOG_FILE_PATH)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(_DEFAULT_FORMATTER)

        # Console handler: controlled by resolved_level
        ch = logging.StreamHandler()
        ch.setLevel(resolved_level)
        ch.setFormatter(_DEFAULT_FORMATTER)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

# Module-level logger convenience (change level via LOG_LEVEL env var or pass explicit arg to get_logger)
logger = get_logger(__name__)