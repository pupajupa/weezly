from typing import Dict, Optional
from domain.category import Category
import slugify
from interfaces.repository import BaseRepository

class CategoryRepository(BaseRepository):
    def __init__(self):
        self.categories = {}
        self.next_category_id = 1

    def create(self, title: str, sub_category: Optional[Category] = None, is_sub: bool = False) -> int:
        new_category_id = self.next_category_id
        new_category = Category(
            _id=new_category_id,
            _title=title,
            _sub_category=sub_category,
            _is_sub=is_sub,
            _slug=slugify.slugify(title)
        )
        self.categories[new_category_id] = new_category
        self.next_category_id += 1
        return new_category_id

    def get(self, category_id: int) -> Optional[Category]:
        return self.categories.get(category_id)

    def update(self, category_id: int, title: str, sub_category: Optional[Category] = None, is_sub: bool = False):
        category = self.categories.get(category_id)
        if category:
            category._title = title
            category._sub_category = sub_category
            category._is_sub = is_sub
            category._slug = slugify.slugify(title)

    def delete(self, category_id: int):
        if category_id in self.categories:
            del self.categories[category_id]

    def list(self) -> Dict[int, Category]:
        return self.categories

    def count(self) -> int:
        return len(self.categories)
