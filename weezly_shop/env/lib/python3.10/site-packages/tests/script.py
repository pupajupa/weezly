import unittest

import user_use_cases_tests
import order_use_cases_tests
import category_use_cases_tests 
import product_use_cases_tests 
import cart_use_cases_tests 

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # Добавление тестов из всех модулей
    suite.addTest(loader.loadTestsFromTestCase(user_use_cases_tests.TestUserUseCases))
    suite.addTest(loader.loadTestsFromTestCase(product_use_cases_tests.TestProductUseCases))
    suite.addTest(loader.loadTestsFromTestCase(cart_use_cases_tests.TestCartUseCases))
    suite.addTest(loader.loadTestsFromTestCase(order_use_cases_tests.TestOrderUseCases))
    suite.addTest(loader.loadTestsFromTestCase(category_use_cases_tests.TestCategoryUseCases))

    # Запуск тестов
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
