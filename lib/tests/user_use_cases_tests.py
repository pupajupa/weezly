import unittest
from unittest.mock import MagicMock
from weezly_lib.domain.user import User
from weezly_lib.use_cases.user_use_cases import CreateUser, ListUsers, GetUser, UpdateUser, DeleteUser

class TestUserUseCases(unittest.TestCase):
    def setUp(self):
        self.mock_user_repository = MagicMock()

    def test_create_user_use_case(self):
        user = User(None, "test@example.com", "password123", "Test User")
        self.mock_user_repository.create.return_value = 1
        create_user_use_case = CreateUser(self.mock_user_repository)

        # Проверяем успешное создание пользователя
        user_id = create_user_use_case.execute(user)
        self.assertEqual(user_id, 1)
        self.mock_user_repository.create.assert_called_once_with(user)

    def test_list_users_use_case(self):
        users_data = [
            User(1, "test1@example.com", "password123", "Test User 1"),
            User(2, "test2@example.com", "password456", "Test User 2"),
            User(3, "test3@example.com", "password789", "Test User 3"),
        ]
        self.mock_user_repository.list.return_value = users_data
        list_users_use_case = ListUsers(self.mock_user_repository)

        # Проверяем успешное получение списка пользователей
        result = list_users_use_case.execute()
        self.assertEqual(result, users_data)

    def test_get_user_use_case(self):
        user_id = 1
        user_data = User(1, "test@example.com", "password123", "Test User")
        self.mock_user_repository.get.return_value = user_data
        get_user_use_case = GetUser(self.mock_user_repository)

        # Проверяем успешное получение пользователя по идентификатору
        result = get_user_use_case.execute(user_id)
        self.assertEqual(result, user_data)

    def test_update_user_use_case(self):
        user = User(1, "test@example.com", "password123", "Updated User")
        self.mock_user_repository.update.return_value = True
        update_user_use_case = UpdateUser(self.mock_user_repository)

        # Проверяем успешное обновление информации о пользователе
        result = update_user_use_case.execute(user)
        self.assertTrue(result)
        self.mock_user_repository.update.assert_called_once_with(user)

    def test_delete_user_use_case(self):
        user_id = 1
        self.mock_user_repository.delete.return_value = True
        delete_user_use_case = DeleteUser(self.mock_user_repository)

        # Проверяем успешное удаление пользователя
        result = delete_user_use_case.execute(user_id)
        self.assertTrue(result)
        self.mock_user_repository.delete.assert_called_once_with(user_id)

if __name__ == "__main__":
    unittest.main()
