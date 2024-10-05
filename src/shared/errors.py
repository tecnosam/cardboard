"""
    Error classes for this module
"""

from typing import Optional
from enum import IntEnum


class ErrorCodes(IntEnum):
    """Error codes supported by the application"""

    GENERIC_CODE = 100
    RESOURCE_NOT_FOUND = 404


class CardboardGenericException(Exception):

    """
    Represents a generic exception
    """

    error_code: int = ErrorCodes.GENERIC_CODE.value
    error_message: str = "An Error has occurred in the system"

    def __init__(self, error_details: Optional[dict] = None):

        self.error_details = error_details or {}
        super().__init__(error_details)
