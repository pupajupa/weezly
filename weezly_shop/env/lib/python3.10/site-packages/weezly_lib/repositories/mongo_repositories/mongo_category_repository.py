from typing import Dict, List, Optional
from pymongo import MongoClient
from domain.category import Category
import slugify
from interfaces.repository import BaseRepository

class MongoDBCategoryRepository(BaseRepository):
    def __init__(self, db_name: str, collection_name: str, uri: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, title: str, sub_category: Optional[Category] = None, is_sub: bool = False) -> str:
        category = Category(
            _id=None,
            _title=title,
            _sub_category=sub_category,
            _is_sub=is_sub,
            _slug=slugify.slugify(title)
        )
        category_dict = category.__dict__
        result = self.collection.insert_one(category_dict)
        return str(result.inserted_id)

    def get(self, category_id: str) -> Optional[Category]:
        category = self.collection.find_one({"_id": category_id})
        if category:
            return Category(**category)
        return None

    def update(self, category_id: str, title: str, sub_category: Optional[Category] = None, is_sub: bool = False):
        update_data = {
            "_title": title,
            "_sub_category": sub_category,
            "_is_sub": is_sub,
            "_slug": slugify.slugify(title)
        }
        self.collection.update_one({"_id": category_id}, {"$set": update_data})

    def delete(self, category_id: str):
        self.collection.delete_one({"_id": category_id})

    def list(self) -> List[Category]:
        categories = self.collection.find()
        return [Category(**category) for category in categories]

    def get_total_categories(self) -> int:
        return self.collection.count_documents({})
