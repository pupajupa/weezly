from typing import Dict, Optional
from domain.category import Category
from repositories.test_repositories.category_repository import CategoryRepository

class CreateCategory:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, title: str, sub_category: Optional[Category] = None, is_sub: bool = False) -> int:
        category_id = self.category_repository.create(title, sub_category, is_sub)
        return category_id

class UpdateCategory:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, category_id: int, title: str, sub_category: Optional[Category] = None, is_sub: bool = False) -> bool:
        self.category_repository.update(category_id, title, sub_category, is_sub)
        return True

class DeleteCategory:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, category_id: int) -> bool:
        self.category_repository.delete(category_id)
        return True

class ListCategories:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self) -> Dict[int, Category]:
        categories = self.category_repository.list()
        return categories

class GetCategory:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, category_id: int) -> Optional[Category]:
        category = self.category_repository.get(category_id)
        return category
