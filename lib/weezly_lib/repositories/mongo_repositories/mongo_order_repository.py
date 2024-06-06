from typing import List, Optional
from pymongo import MongoClient
from domain.order import Order, OrderItem
from domain.user import User 
import datetime
from interfaces.repository import BaseRepository

class MongoDBOrderRepository(BaseRepository):
    def __init__(self, db_name: str, collection_name: str, uri: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, user: User, items: List[OrderItem], status: bool = False) -> str:
        order = Order(
            _id=None,
            _user=user,
            _created=datetime.datetime.now(),
            _updated=datetime.datetime.now(),
            _status=status,
            _items=items
        )
        order_dict = order.__dict__
        result = self.collection.insert_one(order_dict)
        return str(result.inserted_id)

    def get(self, order_id: str) -> Optional[Order]:
        order = self.collection.find_one({"_id": order_id})
        if order:
            return Order(**order)
        return None

    def update(self, order_id: str, status: bool):
        self.collection.update_one({"_id": order_id}, {"$set": {"_status": status, "_updated": datetime.datetime.now()}})

    def delete(self, order_id: str):
        self.collection.delete_one({"_id": order_id})

    def list(self) -> List[Order]:
        orders = self.collection.find()
        return [Order(**order) for order in orders]
