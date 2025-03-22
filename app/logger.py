import sys
import io
from datetime import datetime
from typing import Optional
from loguru import logger as _logger

from app.config import PROJECT_ROOT


_print_level = "INFO"


def define_log_level(print_level="INFO", logfile_level="DEBUG", name: str = None):
    """Adjust the log level to above level"""
    global _print_level
    _print_level = print_level

    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d%H%M%S")
    log_name = (
        f"{name}_{formatted_date}" if name else formatted_date
    )  # name a log with prefix name

    _logger.remove()
    _logger.add(sys.stderr, level=print_level)
    _logger.add(PROJECT_ROOT / f"logs/{log_name}.log", level=logfile_level)
    return _logger


logger = define_log_level()

class LogCapture:
    def __init__(self, level: str = "DEBUG"):
        """
        level: Minimum log level to capture. 
               Use "DEBUG" to get everything, or "INFO" to be more selective.
        """
        self.level = level
        self._log_buffer = io.StringIO()
        self._sink_id: Optional[int] = None

    def start_capture(self):
        """Attach an in-memory sink to the logger."""
        # Loguru's add() returns an ID we need to remove later
        self._sink_id = logger.add(self._log_buffer, level=self.level)

    def stop_capture(self) -> str:
        """Detach the sink and return the captured logs as a string."""
        if self._sink_id is not None:
            logger.remove(self._sink_id)
            self._sink_id = None
        return self._log_buffer.getvalue()

if __name__ == "__main__":
    logger.info("Starting application")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
