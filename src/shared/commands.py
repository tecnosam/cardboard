"""
    DTOs carrying information relevant to how logic should function
"""

from pydantic import BaseModel


class BaseCommand(BaseModel):
    ...


class SampleCommand(BaseCommand):

    name: str
    type: str
    count: int
