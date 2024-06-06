from typing import List, Dict
from domain.product import Product
from domain.category import Category
from repositories.test_repositories.product_repository import ProductRepository

class CreateProduct:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, category: Category, image: str, title: str, description: str, price: int) -> int:
        product_id = self.product_repository.create(category, image, title, description, price)
        return product_id

class UpdateProduct:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int, category: Category, image: str, title: str, description: str, price: int) -> bool:
        self.product_repository.update(product_id, category, image, title, description, price)
        return True

class DeleteProduct:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> bool:
        self.product_repository.delete(product_id)
        return True

class ListProducts:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self) -> Dict[int, Product]:
        products = self.product_repository.list()
        return products

class GetProduct:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> Product:
        product = self.product_repository.get(product_id)
        return product
