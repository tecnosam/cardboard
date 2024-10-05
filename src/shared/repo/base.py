from typing import Any, Optional, Iterable
from abc import ABC, abstractmethod


class AbstractDomainEntityPersistenceRepository(ABC):
    """Abstraction for persisting domain entities"""

    @abstractmethod
    def get(self, uid: Any, *args, **kwargs) -> Optional[Any]:

        """Get a domain entity by it's ID"""

    @abstractmethod
    def fetch_all(self, query: Any) -> Iterable[Any]:
        """Get a list of domain entities based on a filter"""

    @abstractmethod
    def save(self, entity: Any) -> Any:
        """
        Persist the state of the entity's attributes.

        If the domain entity did not exist, create it.
        """

    @abstractmethod
    def delete(self, entity: Any) -> bool:

        """
        Delete a domain entity from persistence layer
        """
