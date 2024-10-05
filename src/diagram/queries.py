from typing import Optional
from pydantic import BaseModel, Field


class BaseQuery(BaseModel):

    offset: Optional[int] = Field(default=0)
    limit: Optional[int] = Field(default=None)
    timestamp: Optional[float]


class DiagramFetchQuery(BaseQuery):

    owner: Optional[str]
    provider_class: Optional[str]
