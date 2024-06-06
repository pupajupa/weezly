from typing import Dict, List, Optional
from domain.product import Product  # Импортируйте свою модель Product
from domain.user import User  # Импортируйте свою модель User
from domain.order import Order, OrderItem  # Импортируйте свои классы Order и OrderItem
import datetime
from interfaces.repository import BaseRepository

class OrderRepository(BaseRepository):
    def __init__(self):
        self.orders = {}
        self.next_order_id = 1

    def create(self, user: User, items: List[OrderItem], status: bool = False) -> int:
        new_order_id = self.next_order_id
        new_order = Order(
            _id=new_order_id,
            _user=user,
            _created=datetime.datetime.now(),
            _updated=datetime.datetime.now(),
            _status=status,
            _items=items
        )
        self.orders[new_order_id] = new_order
        self.next_order_id += 1
        return new_order_id

    def get(self, order_id: int) -> Optional[Order]:
        return self.orders.get(order_id)

    def update(self, order_id: int, status: bool):
        order = self.orders.get(order_id)
        if order:
            order._status = status
            order._updated = datetime.datetime.now()

    def delete(self, order_id: int):
        if order_id in self.orders:
            del self.orders[order_id]

    def list(self) -> Dict[int, Order]:
        return self.orders

    def count(self) -> int:
        return len(self.orders)
