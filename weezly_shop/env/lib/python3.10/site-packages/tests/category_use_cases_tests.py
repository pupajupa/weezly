import unittest
from unittest.mock import MagicMock
from weezly_lib.domain.category import Category
from weezly_lib.use_cases.category_use_cases import CreateCategory, UpdateCategory, DeleteCategory, ListCategories, GetCategory
class TestCategoryUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_category_repository = MagicMock()

    def test_create_category_use_case(self):
        title = "Test Category"
        sub_category = None
        is_sub = False
        create_category_use_case = CreateCategory(self.mock_category_repository)

        # Проверяем успешное создание категории
        category_id = create_category_use_case.execute(title, sub_category, is_sub)
        self.mock_category_repository.create.assert_called_once_with(title, sub_category, is_sub)
        self.assertIsInstance(category_id, int)

    def test_update_category_use_case(self):
        category_id = 1
        title = "Updated Category"
        sub_category = None
        is_sub = False
        update_category_use_case = UpdateCategory(self.mock_category_repository)

        # Проверяем успешное обновление категории
        result = update_category_use_case.execute(category_id, title, sub_category, is_sub)
        self.assertTrue(result)
        self.mock_category_repository.update.assert_called_once_with(category_id, title, sub_category, is_sub)

    def test_delete_category_use_case(self):
        category_id = 1
        delete_category_use_case = DeleteCategory(self.mock_category_repository)

        # Проверяем успешное удаление категории
        result = delete_category_use_case.execute(category_id)
        self.assertTrue(result)
        self.mock_category_repository.delete.assert_called_once_with(category_id)

    def test_list_categories_use_case(self):
        categories_data = {
            1: Category(1, "Category 1"),
            2: Category(2, "Category 2"),
            3: Category(3, "Category 3"),
        }
        self.mock_category_repository.list.return_value = categories_data
        list_categories_use_case = ListCategories(self.mock_category_repository)

        # Проверяем успешное получение списка категорий
        result = list_categories_use_case.execute()
        self.assertEqual(result, categories_data)

    def test_get_category_use_case(self):
        category_id = 1
        category_data = Category(1, "Test Category")
        self.mock_category_repository.get.return_value = category_data
        get_category_use_case = GetCategory(self.mock_category_repository)

        # Проверяем успешное получение категории по идентификатору
        result = get_category_use_case.execute(category_id)
        self.assertEqual(result, category_data)

if __name__ == "__main__":
    unittest.main()
