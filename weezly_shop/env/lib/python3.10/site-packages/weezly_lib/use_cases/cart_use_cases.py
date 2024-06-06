from typing import Dict
from domain.product import Product
from repositories.test_repositories.cart_repository import CartRepository

class AddItemToCart:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self, product: Product, quantity: int):
        self.cart_repository.create(product, quantity)
        return True

class RemoveItemFromCart:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self, product_id: int):
        self.cart_repository.delete(product_id)
        return True

class ClearCart:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self):
        self.cart_repository.clear()
        return True

class GetCartTotalPrice:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self) -> float:
        return self.cart_repository.get_total_price()

class ListCartItems:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self) -> Dict[int, Dict]:
        return self.cart_repository.list()
