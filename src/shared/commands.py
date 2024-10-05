"""
    DTOs carrying information relevant to how logic should function
"""

from pydantic import BaseModel


class BaseCommand(BaseModel):
    """BaseCommand"""


class SampleCommand(BaseCommand):
    """Example Command"""

    name: str
    type: str
    count: int
