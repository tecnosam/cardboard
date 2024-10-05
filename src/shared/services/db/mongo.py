from typing import Optional
from pymongo import MongoClient

from src.config.settings import MONGODB_URI, MONGODB_DBNAME


class MongoDBService:
    """
    Service abstracts mongodb connection logic
    """
    conn_string: str = MONGODB_URI
    database_name: str = MONGODB_DBNAME

    def __init__(self, conn_string: Optional[str] = None, dbname: Optional[str] = None):

        self.conn_string = conn_string or self.conn_string
        self.database_name = dbname or self.database_name

        self.client: MongoClient = MongoClient(self.conn_string)
        self.db = self.client[self.database_name]
