import sys
import os
from unittest.mock import patch
import unittest
from src.api import HHAPI  # Убедитесь, что путь правильный

# Добавляем к PYTHONPATH папку src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestHHAPI(unittest.TestCase):

    @patch('src.api.requests.get')  # Убедитесь, что путь правильный
    def test_get_companies(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'name': 'Company A', 'vacancies_count': 5}

        result = HHAPI.get_companies([1])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Company A')

    @patch('src.api.requests.get')  # Убедитесь, что путь правильный
    def test_get_vacancies(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'items': [{'name': 'Vacancy A', 'salary': {'from': 1000, 'to': 2000}}]
        }

        result = HHAPI.get_vacancies('1')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Vacancy A')


if __name__ == '__main__':
    unittest.main()
