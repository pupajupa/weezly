from dataclasses import dataclass
from typing import List
import datetime
from .user import User
from .product import Product


@dataclass
class OrderItem:
    _id: int
    _product: Product
    _price: int
    _quantity: int

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    
    @property
    def id(self):
        return self._id 
    
    @property
    def product(self):
        return self._product 

    @property
    def price(self):
        return self._price 

    @property
    def quantity(self):
        return self._quantity 

@dataclass
class Order:
    _id: int
    _user: User
    _created: datetime
    _updated: datetime
    _status: bool
    _items: List[OrderItem] = None

    @property
    def id(self):
        return self._id 
    @property
    def user(self):
        return self._user 
    @property
    def created(self):
        return self._created 
    @property
    def updated(self):
        return self._updated 
    @property
    def status(self):
        return self._status 
    @property
    def items(self):
        return self._items 
    
    def __str__(self):
        return f"{self.user.full_name} - order id: {self.id}"

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items)
        return total

    def add_items(self, items: List[OrderItem]):
        self._items = items


def link_order_to_order_items(order: Order, items: List[OrderItem]):
    order.add_items(items)

