import sys
import traceback
from typing import Any, Optional
from src.logger import logging

def error_message_detail(error: Exception, error_detail: Optional[Any] = None) -> str:
    """
    Build a detailed error message including file and line number.
    If error_detail is None, use sys.exc_info().
    """
    if error_detail is None:
        error_detail = sys

    exc_type, exc_value, exc_tb = error_detail.exc_info()
    if exc_tb is not None:
        # get last traceback frame (where exception was raised)
        tb_frame = exc_tb.tb_frame
        file_name = tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno
    else:
        file_name = "<unknown>"
        line_no = 0

    return f"Error occurred in python script name [{file_name}] line number [{line_no}] error message [{error}]"

class CustomException(Exception):
    """
    Exception wrapper that stores a formatted error message and the original exception.
    """
    def __init__(self, error: Exception, error_detail: Optional[Any] = None):
        super().__init__(error)
        self.original_exception = error
        self.error_message = error_message_detail(error, error_detail=error_detail)
        # optionally log the exception with traceback
        logging.error(self.error_message)
        # If you want the full stack trace logged:
        logging.debug("".join(traceback.format_exception(* (error_detail.exc_info() if error_detail else sys.exc_info()))))

    def __str__(self) -> str:
        return self.error_message