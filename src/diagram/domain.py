from typing import Optional, List
from pydantic import BaseModel, Field

from uuid import UUID, uuid4


class Base(BaseModel):

    uid: UUID = Field(default_factory=uuid4)



class Node(Base):

    """
    Represents a Node that can be connected to another Node
    """

    name: str
    metadata: dict = Field(default_factory=dict)  # Aditional provisioning configurations


class Edge(Base):

    """
    Represents a connection between two resources or a resource and a cluster
    """

    tag: str

    start_node_uid: UUID
    end_node_uid: UUID

    is_bidirectional: bool = False  # Is this a bidirectional edge?


class Diagram(Base):

    name: str
    owner: Optional[str] = None

    provider_class: str  # What kind of diagram is this (AWS, Azure, GCP, K8s, ERD, etc)

    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)


# Node classes

class Cluster(Node):
    """
    Represents a group of Resources or other clusters.
    """

    node_type: str = "cluster"
    children: List[Node] = Field(default_factory=list)


class Resource(Node):

    """
    Represents a single resource. Could be part of a cluster
    """

    node_type: str = "resource"
    resource_class: str  # What kind of resource is this (e.g AWS EC2, Azure Container Registry, K8 Pod)
