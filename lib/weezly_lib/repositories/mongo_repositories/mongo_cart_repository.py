from typing import List, Optional,Dict
from pymongo import MongoClient
from domain.product import Product
from interfaces.repository import BaseRepository

class MongoDBCartRepository(BaseRepository):
    def __init__(self, db_name: str, collection_name: str, uri: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_item(self, product: Product, quantity: int):
        product_id = product.id
        existing_item = self.collection.find_one({"_id": product_id})
        if existing_item:
            new_quantity = existing_item['quantity'] + quantity
            self.collection.update_one({"_id": product_id}, {"$set": {"quantity": new_quantity}})
        else:
            item = {
                "_id": product_id,
                "product": product,
                "quantity": quantity,
                "price": product.price
            }
            self.collection.insert_one(item)

    def remove_item(self, product_id: int):
        self.collection.delete_one({"_id": product_id})

    def clear(self):
        self.collection.delete_many({})

    def get_total_price(self) -> float:
        items = self.collection.find()
        total_price = sum(item['price'] * item['quantity'] for item in items)
        return total_price

    def get_items(self) -> Dict[int, int]:
        items = self.collection.find()
        return {item['_id']: item['quantity'] for item in items}
