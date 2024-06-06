import unittest
from unittest.mock import MagicMock
from weezly_lib.domain.user import User
from weezly_lib.domain.order import Order, OrderItem
from weezly_lib.use_cases.order_use_cases import CreateOrder, UpdateOrderStatus, DeleteOrder, ListOrders, GetOrder

class TestOrderUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_order_repository = MagicMock()

    def test_create_order_use_case(self):
        user = User(1, "Test User")
        items = [
            OrderItem(1, "Product 1", 10, 2),
            OrderItem(2, "Product 2", 20, 1)
        ]
        status = False
        create_order_use_case = CreateOrder(self.mock_order_repository)

        # Проверяем успешное создание заказа
        order_id = create_order_use_case.execute(user, items, status)
        self.mock_order_repository.create.assert_called_once_with(user, items, status)
        self.assertIsInstance(order_id, int)

    def test_update_order_status_use_case(self):
        order_id = 1
        status = True
        update_order_status_use_case = UpdateOrderStatus(self.mock_order_repository)

        # Проверяем успешное обновление статуса заказа
        result = update_order_status_use_case.execute(order_id, status)
        self.assertTrue(result)
        self.mock_order_repository.update.assert_called_once_with(order_id, status)

    def test_delete_order_use_case(self):
        order_id = 1
        delete_order_use_case = DeleteOrder(self.mock_order_repository)

        # Проверяем успешное удаление заказа
        result = delete_order_use_case.execute(order_id)
        self.assertTrue(result)
        self.mock_order_repository.delete.assert_called_once_with(order_id)

    def test_list_orders_use_case(self):
        orders_data = {
            1: Order(1, "Test User", False, []),
            2: Order(2, "Test User", True, []),
            3: Order(3, "Test User", False, [])
        }
        self.mock_order_repository.list.return_value = orders_data
        list_orders_use_case = ListOrders(self.mock_order_repository)

        # Проверяем успешное получение списка заказов
        result = list_orders_use_case.execute()
        self.assertEqual(result, orders_data)

    def test_get_order_use_case(self):
        order_id = 1
        order_data = Order(1, "Test User", False, [])
        self.mock_order_repository.get.return_value = order_data
        get_order_use_case = GetOrder(self.mock_order_repository)

        # Проверяем успешное получение заказа по идентификатору
        result = get_order_use_case.execute(order_id)
        self.assertEqual(result, order_data)

if __name__ == "__main__":
    unittest.main()
