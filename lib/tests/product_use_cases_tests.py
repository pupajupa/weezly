import unittest
from unittest.mock import MagicMock
from weezly_lib.domain.product import Product, Category
from weezly_lib.use_cases.product_use_cases import CreateProduct, UpdateProduct, DeleteProduct, ListProducts, GetProduct

class TestProductUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_product_repository = MagicMock()

    def test_create_product_use_case(self):
        category = Category(1, "Test Category")
        image = "test_image.jpg"
        title = "Test Product"
        description = "Test Description"
        price = 100
        create_product_use_case = CreateProduct(self.mock_product_repository)

        # Проверяем успешное создание продукта
        product_id = create_product_use_case.execute(category, image, title, description, price)
        self.mock_product_repository.create.assert_called_once_with(category, image, title, description, price)
        self.assertIsInstance(product_id, int)

    def test_update_product_use_case(self):
        product_id = 1
        category = Category(1, "Test Category")
        image = "updated_image.jpg"
        title = "Updated Product"
        description = "Updated Description"
        price = 200
        update_product_use_case = UpdateProduct(self.mock_product_repository)

        # Проверяем успешное обновление продукта
        result = update_product_use_case.execute(product_id, category, image, title, description, price)
        self.assertTrue(result)
        self.mock_product_repository.update.assert_called_once_with(product_id, category, image, title, description, price)

    def test_delete_product_use_case(self):
        product_id = 1
        delete_product_use_case = DeleteProduct(self.mock_product_repository)

        # Проверяем успешное удаление продукта
        result = delete_product_use_case.execute(product_id)
        self.assertTrue(result)
        self.mock_product_repository.delete.assert_called_once_with(product_id)

    def test_list_products_use_case(self):
        products_data = {
            1: Product(1, "Test Product 1", "Test Description 1", 100),
            2: Product(2, "Test Product 2", "Test Description 2", 200),
            3: Product(3, "Test Product 3", "Test Description 3", 300)
        }
        self.mock_product_repository.list.return_value = products_data
        list_products_use_case = ListProducts(self.mock_product_repository)

        # Проверяем успешное получение списка продуктов
        result = list_products_use_case.execute()
        self.assertEqual(result, products_data)

    def test_get_product_use_case(self):
        product_id = 1
        product_data = Product(1, "Test Product", "Test Description", 100)
        self.mock_product_repository.get.return_value = product_data
        get_product_use_case = GetProduct(self.mock_product_repository)

        # Проверяем успешное получение продукта по идентификатору
        result = get_product_use_case.execute(product_id)
        self.assertEqual(result, product_data)

if __name__ == "__main__":
    unittest.main()
