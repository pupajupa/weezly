from typing import Dict
from domain.product import Product  # Импортируйте свою модель Product
from interfaces.repository import BaseRepository


class CartRepository(BaseRepository):
    def __init__(self):
        self.cart_items = {}

    def create(self, product: Product, quantity: int):
        product_id = product.id
        if product_id in self.cart_items:
            self.cart_items[product_id]['quantity'] += quantity
        else:
            self.cart_items[product_id] = {
                'product': product,
                'quantity': quantity,
                'price': product.price
            }

    def get(self, product_id: int) -> Dict:
        return self.cart_items.get(product_id)

    def update(self, product: Product, quantity: int):
        product_id = product.id
        if product_id in self.cart_items:
            self.cart_items[product_id]['quantity'] = quantity

    def delete(self, product_id: int):
        if product_id in self.cart_items:
            del self.cart_items[product_id]

    def list(self) -> Dict[int, Dict]:
        return self.cart_items

    def clear(self):
        self.cart_items = {}

    def get_total_price(self) -> float:
        total_price = 0
        for item in self.cart_items.values():
            total_price += item['price'] * item['quantity']
        return total_price
