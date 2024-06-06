from typing import List, Optional
from pymongo import MongoClient
from domain.product import Product
from domain.category import Category
import datetime,slugify
from interfaces.repository import BaseRepository

class MongoDBProductRepository(BaseRepository):
    def __init__(self, db_name: str, collection_name: str, uri: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, category: Category, image: str, title: str, description: str, price: int) -> str:
        product = Product(
            _id=None,
            _category=category,
            _image=image,
            _title=title,
            _description=description,
            _price=price,
            _date_created=datetime.datetime.now(),
            _slug=slugify.slugify(title)
        )
        product_dict = product.__dict__
        result = self.collection.insert_one(product_dict)
        return str(result.inserted_id)

    def get(self, product_id: str) -> Optional[Product]:
        product = self.collection.find_one({"_id": product_id})
        if product:
            return Product(**product)
        return None

    def update(self, product_id: str, category: Category, image: str, title: str, description: str, price: int):
        update_data = {
            "_category": category,
            "_image": image,
            "_title": title,
            "_description": description,
            "_price": price,
            "_date_created": datetime.datetime.now(),
            "_slug": slugify.slugify(title)
        }
        self.collection.update_one({"_id": product_id}, {"$set": update_data})

    def delete(self, product_id: str):
        self.collection.delete_one({"_id": product_id})

    def list(self) -> List[Product]:
        products = self.collection.find()
        return [Product(**product) for product in products]
