from typing import List, Optional
from pymongo import MongoClient
from domain.user import User
from interfaces.repository import BaseRepository

class MongoDBUserRepository(BaseRepository):
    def __init__(self, db_name: str, collection_name: str, uri: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, user: User) -> int:
        user_dict = user.__dict__
        result = self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    def list(self) -> List[User]:
        users = self.collection.find()
        return [User(**user) for user in users]

    def get(self, user_id: str) -> Optional[User]:
        user = self.collection.find_one({"_id": user_id})
        if user:
            return User(**user)
        return None

    def update(self, user: User):
        self.collection.update_one({"_id": user.id}, {"$set": user.__dict__})

    def delete(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
