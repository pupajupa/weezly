from typing import List, Dict, Optional
from domain.user import User
from domain.order import Order, OrderItem
from repositories.test_repositories.order_repository import OrderRepository

class CreateOrder:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, user: User, items: List[OrderItem], status: bool = False) -> int:
        order_id = self.order_repository.create(user, items, status)
        return order_id

class UpdateOrderStatus:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: int, status: bool) -> bool:
        self.order_repository.update(order_id, status)
        return True

class DeleteOrder:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: int) -> bool:
        self.order_repository.delete(order_id)
        return True

class ListOrders:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self) -> Dict[int, Order]:
        orders = self.order_repository.list()
        return orders

class GetOrder:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: int) -> Optional[Order]:
        order = self.order_repository.get(order_id)
        return order
