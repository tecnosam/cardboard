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
        data = self.unify_diagram_nodes(data=data)

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

    @classmethod
    def unify_diagram_nodes(cls, data: dict) -> dict:

        """
        This helper function helps us to merge clusters and resources
        together as one list recursively (also resolves nested clusters)
        """

        nodes = [*data.pop("resources", [])]

        for child_cluster in data.pop("clusters", []):
            nodes.append(cls.unify_diagram_nodes(child_cluster))

        data["nodes"] = nodes
        return data
