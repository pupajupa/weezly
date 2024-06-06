from typing import Dict
from dataclasses import dataclass
from .product import Product # Импортируйте свою модель Product

@dataclass
class CartItem:
    _id: int
    _product: Product
    _quantity: int
    _price: float
    _total_price: float

    @property
    def id(self):
        return self._id

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def total_price(self):
        return self._total_price


@dataclass
class Cart:
    _id: int
    _items: Dict[int, CartItem] = {}

    @property
    def id(self):
        return self._id
    
    @property
    def items(self):
        return self._items

    