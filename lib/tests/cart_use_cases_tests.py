import unittest
from unittest.mock import MagicMock
from weezly_lib.domain.product import Product
from weezly_lib.repositories.test_repositories.cart_repository import CartRepository
from weezly_lib.use_cases.cart_use_cases import AddItemToCart, RemoveItemFromCart, ClearCart, GetCartTotalPrice, ListCartItems

class TestCartUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_cart_repository = MagicMock()

    def test_add_item_to_cart_use_case(self):
        product = Product(1, "Test Product", "Description", 10)
        quantity = 2
        add_item_to_cart_use_case = AddItemToCart(self.mock_cart_repository)

        # Проверяем успешное добавление товара в корзину
        add_item_to_cart_use_case.execute(product, quantity)
        self.mock_cart_repository.create.assert_called_once_with(product, quantity)

    def test_remove_item_from_cart_use_case(self):
        product_id = 1
        remove_item_from_cart_use_case = RemoveItemFromCart(self.mock_cart_repository)

        # Проверяем успешное удаление товара из корзины
        remove_item_from_cart_use_case.execute(product_id)
        self.mock_cart_repository.delete.assert_called_once_with(product_id)

    def test_clear_cart_use_case(self):
        clear_cart_use_case = ClearCart(self.mock_cart_repository)

        # Проверяем успешную очистку корзины
        clear_cart_use_case.execute()
        self.mock_cart_repository.clear.assert_called_once()

    def test_get_cart_total_price_use_case(self):
        total_price = 50.0
        self.mock_cart_repository.get_total_price.return_value = total_price
        get_cart_total_price_use_case = GetCartTotalPrice(self.mock_cart_repository)

        # Проверяем успешное получение общей стоимости корзины
        result = get_cart_total_price_use_case.execute()
        self.assertEqual(result, total_price)

    def test_list_cart_items_use_case(self):
        items_data = {1: {"product": Product(1, "Test Product", "Description", 10), "quantity": 2}}
        self.mock_cart_repository.list.return_value = items_data
        list_cart_items_use_case = ListCartItems(self.mock_cart_repository)

        # Проверяем успешное получение списка товаров в корзине
        result = list_cart_items_use_case.execute()
        self.assertEqual(result, items_data)

if __name__ == "__main__":
    unittest.main()
