import unittest
from unittest.mock import patch
from src.api import HHAPI


class TestHHAPI(unittest.TestCase):
    """Тесты для класса HHAPI."""

    @patch('src.api.requests.get')
    def test_get_companies(self, mock_get):
        """Тестирует получение информации о компаниях."""
        # Настройка mock-объекта
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'name': 'Test Company'}

        result = HHAPI.get_companies(['1'])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test Company')

    @patch('src.api.requests.get')
    def test_get_vacancies(self, mock_get):
        """Тестирует получение списка вакансий по идентификатору компании."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'items': [{'name': 'Test Vacancy'}]}

        result = HHAPI.get_vacancies('1')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test Vacancy')


if __name__ == '__main__':
    unittest.main()
