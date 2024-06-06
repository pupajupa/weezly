from typing import Dict, List, Optional
from domain.user import User
from interfaces.repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.next_id: int = 1

    def create(self, user: User) -> int:
        user._id = self.next_id
        self.users[self.next_id] = user
        self.next_id += 1
        return user._id

    def list(self) -> List[User]:
        return list(self.users.values())

    def get(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def update(self, user: User):
        if user._id in self.users:
            self.users[user._id] = user

    def delete(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
