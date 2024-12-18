import unittest
from unittest.mock import MagicMock
from src.db import Database
from src.db_manager import DBManager


class TestDBManager(unittest.TestCase):
    """Тесты для класса DBManager."""

    def setUp(self):
        """Настройка тестового окружения для класса DBManager."""
        self.mock_db = MagicMock()
        self.db_manager = DBManager(self.mock_db)

    def test_get_companies_and_vacancies_count(self):
        """Тестирует получение списка компаний и количества их вакансий."""
        self.mock_db.cursor.return_value.fetchall.return_value = [('Test Company', 2)]

        result = self.db_manager.get_companies_and_vacancies_count()

        self.assertEqual(result, [('Test Company', 2)])

    def test_get_all_vacancies(self):
        """Тестирует получение списка всех вакансий с указанием названия компании."""
        self.mock_db.cursor.return_value.fetchall.return_value = [('Test Vacancy', 'Test Company', 1000, 2000)]

        result = self.db_manager.get_all_vacancies()

        self.assertEqual(result, [('Test Vacancy', 'Test Company', 1000, 2000)])


if __name__ == '__main__':
    unittest.main()
    