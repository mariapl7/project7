import unittest
from unittest.mock import MagicMock
from src.db_manager import DBManager


class TestDBManager(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.db_manager = DBManager(self.mock_db)

    def test_get_companies_and_vacancies_count(self):
        self.mock_db.cursor.fetchall.return_value = [('Company A', 5)]

        result = self.db_manager.get_companies_and_vacancies_count()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'Company A')
        self.assertEqual(result[0][1], 5)

    def test_get_all_vacancies(self):
        self.mock_db.cursor.fetchall.return_value = [('Vacancy A', 'Company A', 1000, 2000)]

        result = self.db_manager.get_all_vacancies()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'Vacancy A')


if __name__ == '__main__':
    unittest.main()
    