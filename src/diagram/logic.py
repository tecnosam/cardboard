from abc import ABC, abstractmethod

from typing import List, Type, Any, Union

from src.shared.repo.base import AbstractDomainEntityPersistenceRepository
from src.diagram.repo.base import AbstractDiagramPersistenceRepository
from src.diagram.commands import (
    AbstractCommand,
    DiagramCreateCommand,
    DiagramUpdateCommand,
    ClusterCreateCommand,
    ClusterUpdateCommand,
    ResourceCreateCommand,
    ResourceUpdateCommand,
    EdgeCreateCommand,
    EdgeUpdateCommand,
    NodeUpdateCommand
)

from src.diagram.queries import (
    BaseQuery,
    DiagramFetchQuery
)

from src.diagram.domain import (
    Diagram,
    Cluster,
    Resource,
    Node,
    Edge
)

from src.diagram.errors import(
    DiagramNotFoundError,
    NodeNotFoundError,
    EdgeNotFoundError
)


class CRUDLogic(ABC):

    def __init__(self, store_repo: AbstractDomainEntityPersistenceRepository):

        self.store_repo = store_repo

    @abstractmethod
    def create(self, command):
        """Create a new document"""

    @abstractmethod
    def get(self, uid: str):
        """Get a specific document from the database"""

    @abstractmethod
    def fetch_all(self, query: Any):

        """
            Fetch all documents
        """

    @abstractmethod
    def update(self, command):
        """Update a document"""

    @abstractmethod
    def delete(self, uid: str):

        """
            Delete a document with the UID
        """


class DiagramCRUDLogic(CRUDLogic):

    def __init__(self, store_repo: AbstractDiagramPersistenceRepository):

        super().__init__(store_repo=store_repo)

    def create(self, command: DiagramCreateCommand) -> dict:

        """
            Create a diagram and store
        """

        data = command.model_dump()
        data["provider_class"] = command.provider_class.value

        diagram = Diagram(**data)
        self.store_repo.save(diagram)

        return {"uid": diagram.uid}

    def get(self, uid: str) -> Diagram:

        diagram = self.store_repo.get(uid)

        if not diagram:

            raise DiagramNotFoundError

        return diagram

    def fetch_all(self, query: DiagramFetchQuery) -> List[Diagram]:
        """
        Fetch all diagrams that fit the matching query
        """

        query_data = query.model_dump(exclude_unset=True)
        return list(self.store_repo.fetch_all(query_data))

    def update(self, command: DiagramUpdateCommand) -> bool:

        """
        Update a diagram's basic information
        """

        diagram = self.store_repo.get(command.uid)

        updates = command.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(diagram, key, value)

        self.store_repo.save(diagram)
        return True

    def delete(self, uid: str) -> bool:

        """
        Delete a diagram
        """

        diagram = self.store_repo.get(uid)

        if not diagram:
            raise DiagramNotFoundError

        self.store_repo.delete(diagram)

        return True


class NodeCRUDLogic(CRUDLogic):

    node_class: Type[Node]

    def create(self, command: Union[ClusterCreateCommand, ResourceCreateCommand]) -> dict:

        """
            Create a node and persist
        """

        data = command.model_dump()

        node = self.node_class(**data)
        self.store_repo.save(node)

        return {"uid": node.uid}

    def get(self, uid: str) -> Union[Cluster, Resource]:

        node = self.store_repo.get(uid)

        if not node:
            raise NodeNotFoundError(node_type=self.node_class.__name__)

        return node

    def update(self, command: Union[ClusterUpdateCommand, ResourceUpdateCommand]) -> bool:

        """
        Update a node's basic information
        """

        node = self.store_repo.get(command.uid)

        updates = command.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(node, key, value)

        self.store_repo.save(node)
        return True

    def delete(self, uid: str) -> bool:

        """
        Delete a node
        """

        node = self.store_repo.get(uid)

        if not node:
            raise NodeNotFoundError(node_type=self.node_class.__name__)

        self.store_repo.delete(node)

        return True


class ClusterCRUDLogic(NodeCRUDLogic):
    
    """
    Logic layer for managing clusters
    """

    node_class: Type[Node] = Cluster


class ResourceCRUDLogic(NodeCRUDLogic):
    """
    Logic layer for managing resources in diagrams
    """

    node_class: Type[Node] = Resource


class EdgeCRUDLogic(CRUDLogic):
    """Logic layer for managing edges"""

    def create(self, command: EdgeCreateCommand) -> dict:

        """
            Create a edge and persist
        """

        data = command.model_dump()

        edge = Edge(**data)
        self.store_repo.save(edge)

        return {"uid": edge.uid}

    def get(self, uid: str) -> Edge:
        """Get an edge from persistence layer"""

        edge = self.store_repo.get(uid)

        if not edge:
            raise EdgeNotFoundError

        return edge

    def update(self, command: EdgeUpdateCommand) -> bool:

        """
        Update an edge's basic information
        """

        edge = self.store_repo.get(command.uid)

        updates = command.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(edge, key, value)

        self.store_repo.save(edge)
        return True

    def delete(self, uid: str) -> bool:

        """
        Delete an edge
        """

        edge = self.store_repo.get(uid)

        if not edge:
            raise EdgeNotFoundError

        self.store_repo.delete(edge)

        return True
