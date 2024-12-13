import unittest
from unittest.mock import patch
from src.api import HHAPI


class TestHHAPI(unittest.TestCase):

    @patch('api.requests.get')
    def test_get_companies(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'name': 'Company A', 'vacancies_count': 5}

        result = HHAPI.get_companies([1])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Company A')

    @patch('api.requests.get')
    def test_get_vacancies(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'items': [{'name': 'Vacancy A', 'salary': {'from': 1000, 'to': 2000}}]}

        result = HHAPI.get_vacancies('1')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Vacancy A')


if __name__ == '__main__':
    unittest.main()
