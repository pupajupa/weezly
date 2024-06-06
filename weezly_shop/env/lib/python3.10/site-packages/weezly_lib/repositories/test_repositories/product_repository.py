from typing import Dict, Optional
from domain.product import Product
from domain.category import Category
from interfaces.repository import BaseRepository
import datetime
import slugify

class ProductRepository(BaseRepository):
    def __init__(self):
        self.products = {}
        self.next_product_id = 1

    def create(self, category: Category, image: str, title: str, description: str, price: int) -> int:
        new_product_id = self.next_product_id
        new_product = Product(
            _id=new_product_id,
            _category=category,
            _image=image,
            _title=title,
            _description=description,
            _price=price,
            _date_created=datetime.datetime.now(),
            _slug=slugify.slugify(title)
        )
        self.products[new_product_id] = new_product
        self.next_product_id += 1
        return new_product_id

    def get(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)

    def update(self, product_id: int, category: Category, image: str, title: str, description: str, price: int):
        product = self.products.get(product_id)
        if product:
            product._category = category
            product._image = image
            product._title = title
            product._description = description
            product._price = price
            product._date_created = datetime.datetime.now()
            product._slug = slugify.slugify(title)

    def delete(self, product_id: int):
        if product_id in self.products:
            del self.products[product_id]

    def list(self) -> Dict[int, Product]:
        return self.products

    def count(self) -> int:
        return len(self.products)
