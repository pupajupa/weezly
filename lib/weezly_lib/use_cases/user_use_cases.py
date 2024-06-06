from typing import Optional, List
from weezly_lib.domain.user import User
from repositories.test_repositories.user_repository import UserRepository

class CreateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user: User) -> int:
        return self.user_repository.create(user)

class ListUsers:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        return self.user_repository.list()

class GetUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> Optional[User]:
        return self.user_repository.get(user_id)

class UpdateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user: User):
        self.user_repository.update(user)
        return True

class DeleteUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)
