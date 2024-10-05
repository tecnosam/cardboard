
from typing import Optional, Type
from pydantic import BaseModel

from src.diagram.domain import Diagram, Node, Cluster, Resource
from src.shared.repo.mongo import BaseMongoDBCollectionPersistenceRepository


class DiagramMongoDBPersistenceRepository(BaseMongoDBCollectionPersistenceRepository):

    domain_entity_class: Type[BaseModel] = Diagram
    collection_name: str = "diagrams"

    @classmethod
    def document_to_entity(cls, document: dict) -> Diagram:

        keys = ["name", "owner", "provider_class"]
        values = {key: document[key] for key in keys if key in document}

        diagram = Diagram(**values)
        nodes = []

        for node in document.get("nodes", []):

            if node.get("node_type") == "cluster":
                nodes.append(Cluster(**node))
            elif node.get("node_type") == "resource":
                nodes.append(Resource(**node))
            else:
                nodes.append(Node(**node))

        diagram.nodes = nodes
        return diagram
