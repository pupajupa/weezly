from dataclasses import dataclass
from typing import Optional
import slugify

@dataclass
class Category:
    _id: int = None
    _title: str
    _sub_category: Optional['Category'] = None
    _is_sub: bool = False
    _slug: str = None

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title
    
    @property
    def sub_category(self):
        return self._sub_category
    
    @property
    def is_sub(self):
        return self._is_sub
    
    @property
    def slug(self):
        return self._slug
    
    def __post_init__(self):
        self.slug = slugify(self.title)