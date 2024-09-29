"""
    Error classes for this module
"""

from enum import IntEnum


class ErrorCodes(IntEnum):

    GENERIC_CODE = 100


class CardboardGenericException(Exception):

    """
    Represents a generic exception
    """

    error_code: int = ErrorCodes.GENERIC_CODE.value
    error_message: str = "An Error has occurred in the system"

    def __init__(self, error_details):

        self.error_details = error_details
        super().__init__(error_details)
