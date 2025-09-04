import sys
import traceback
from typing import Optional, Union


class EstateRAGException(Exception):
    """
    Base exception class for EstateRAG Assistant.
    Captures detailed traceback, file location, and line number for diagnostics.
    """

    def __init__(self, error_message: Union[str, BaseException], error_details: Optional[object] = None):
        self.error_message = str(error_message)

        # Resolve traceback info
        exc_type, exc_value, exc_tb = None, None, None
        if error_details is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        elif hasattr(error_details, "exc_info"):
            exc_type, exc_value, exc_tb = error_details.exc_info()
        elif isinstance(error_details, BaseException):
            exc_type, exc_value, exc_tb = type(error_details), error_details, error_details.__traceback__
        else:
            exc_type, exc_value, exc_tb = sys.exc_info()

        # Traverse to last traceback frame
        last_tb = exc_tb
        while last_tb and last_tb.tb_next:
            last_tb = last_tb.tb_next

        self.file_name = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
        self.line_number = last_tb.tb_lineno if last_tb else -1

        # Format traceback
        self.traceback_str = (
            ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
            if exc_type and exc_tb else ""
        )

        super().__init__(self.__str__())

    def __str__(self):
        base = f"[EstateRAGException] File: {self.file_name}, Line: {self.line_number}, Message: {self.error_message}"
        if self.traceback_str:
            return f"{base}\nTraceback:\n{self.traceback_str}"
        return base

    def __repr__(self):
        return f"EstateRAGException(file={self.file_name!r}, line={self.line_number}, message={self.error_message!r})"
