from abc import ABC, abstractmethod

from typing import Iterable, Optional
from src.shared.repo.base import AbstractDomainEntityPersistenceRepository
from src.diagram.domain import Diagram


class AbstractDiagramPersistenceRepository(AbstractDomainEntityPersistenceRepository, ABC):
    """
    Abstract interface for persisting diagrams
    """

    @abstractmethod
    def get(self, uid: str) -> Optional[Diagram]:
        """Get a diagram by it's ID"""

    @abstractmethod
    def fetch_all(self, query: dict) -> Iterable[Diagram]:
        """Get a list of domain entities based on a filter"""

    @abstractmethod
    def save(self, entity: Diagram) -> Diagram:
        """
        Persist the state of the entity's attributes.

        If the diagram did not exist, create it.
        """

    @abstractmethod
    def delete(self, entity: Diagram) -> bool:

        """
        Delete a diagram from persistence layer
        """
