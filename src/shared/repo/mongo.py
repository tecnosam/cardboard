
from typing import Optional, Type, Iterable
from pydantic import BaseModel

from src.diagram.domain import Diagram
from src.shared.services.db.mongo import MongoDBService
from src.shared.repo.base import AbstractDomainEntityPersistenceRepository


class BaseMongoDBCollectionPersistenceRepository(AbstractDomainEntityPersistenceRepository):

    """Allows us to persist documents to mongodb"""

    domain_entity_class: Type[BaseModel] = BaseModel
    collection_name: str = ""

    def __init__(self, service: MongoDBService):
        self.service = service
        self.collection = self.service.db[self.collection_name]

    def get(self, uid: str) -> Optional[BaseModel]:
        """
        Get a entity by it's ID
        """

        document = self.collection.find_one({"uid": uid})

        if not document:
            return None
        return self.document_to_entity(document)

    def fetch_all(self, query: dict) -> Iterable[BaseModel]:
        """
        Get all diagrams based on search query
        """

        offset = query.pop("offset", 0)
        limit = query.pop("limit", 0)

        documents = self.collection.find(query, skip=offset, limit=limit)

        for document in documents:
            yield self.document_to_entity(document=document)

    def save(self, entity: Diagram) -> bool:
        """
        Persist the entity to mongodb
        """

        document = entity.model_dump()
        result = self.collection.update_one(
            {"uid": entity.uid},
            {"$set": document},
            upsert=True
        )

        return result.modified_count > 0  and result.acknowledged

    def delete(self, entity: Diagram) -> bool:
        """Delete a entity from mongodb"""

        result = self.collection.delete_one({"uid": entity.uid})
        return result.deleted_count > 0 and result.acknowledged

    @classmethod
    def document_to_entity(cls, document: dict) -> BaseModel:
        """Converts entity document (dict) to a Diagram domain entity"""

        keys = cls.domain_entity_class.schema()["properties"].keys()
        document = {key: document[key] for key in keys if key in document}

        return cls.domain_entity_class(**document)
