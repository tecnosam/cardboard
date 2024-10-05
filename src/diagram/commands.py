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


class ResourceCreateCommand(AbstractCommand):

    name: str
    resource_class: str
    metadata: dict = Field(default_factory=dict)


class ClusterCreateCommand(AbstractCommand):

    name: str
    metadata: dict = Field(default_factory=dict)
    resources: List[ResourceCreateCommand] = Field(default_factory=list)
    clusters: List["ClusterCreateCommand"] = Field(default_factory=list)


class EdgeCreateCommand(AbstractCommand):

    tag: str

    start_node_uid: UUID
    end_node_uid: UUID
    is_bidirectional: bool = False


class DiagramCreateCommand(AbstractCommand):

    name: str
    owner: Optional[str] = Field(default=None)
    provider_class: ProviderClass

    edges: List[EdgeCreateCommand] = Field(default_factory=list)
    clusters: List[ClusterCreateCommand] = Field(default_factory=list)
    resources: List[ResourceCreateCommand] = Field(default_factory=list)


class DiagramUpdateCommand(AbstractCommand):

    uid: str
    name: Optional[str]
    owner: Optional[str]
    provider_class: Optional[str]

    edges: List[EdgeCreateCommand] = Field(default_factory=list)
    clusters: List[ClusterCreateCommand] = Field(default_factory=list)
    resources: List[ResourceCreateCommand] = Field(default_factory=list)
