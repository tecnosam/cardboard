from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AbstractCommand(BaseModel):
    ...


class ProviderClass(Enum):

    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    KUBERNETES = "k8s"

    ERD = "erd"

    CUSTOM = "custom"


class DiagramCreateCommand(AbstractCommand):

    name: str
    owner: Optional[str] = Field(default=None)
    provider_class: ProviderClass


class DiagramUpdateCommand(AbstractCommand):

    uid: str
    name: Optional[str]
    owner: Optional[str]
    provider_class: Optional[str]


class ClusterCreateCommand(AbstractCommand):

    name: str
    metadata: dict


class NodeUpdateCommand(AbstractCommand):

    uid: str


class ClusterUpdateCommand(NodeUpdateCommand):

    name: Optional[str]
    metadata: dict = Field(default_factory=lambda: {})


class ResourceCreateCommand(AbstractCommand):

    name: str
    resource_class: str
    metadata: dict = Field(default_factory=lambda: {})


class ResourceUpdateCommand(NodeUpdateCommand):

    name: Optional[str]
    resource_class: Optional[str]
    metadata: dict = Field(default_factory=lambda: {})


class EdgeCreateCommand(AbstractCommand):

    ...


class EdgeUpdateCommand(AbstractCommand):

    uid: str
