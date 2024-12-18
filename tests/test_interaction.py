import unittest
from unittest.mock import MagicMock, patch
import unittest
from io import StringIO
from unittest.mock import patch

from src.interaction import print_companies_and_vacancies, print_all_vacancies


class TestInteraction(unittest.TestCase):
    """Тесты для функций взаимодействия с пользователем."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_companies_and_vacancies(self, mock_stdout):
        """Тестирует печать компаний и количества их вакансий."""
        print_companies_and_vacancies([('Company A', 5), ('Company B', 10)])
        output = mock_stdout.getvalue()
        self.assertIn('Company A: 5 вакансий', output)
        self.assertIn('Company B: 10 вакансий', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_all_vacancies(self, mock_stdout):
        """Тестирует печать списка всех вакансий."""
        print_all_vacancies([('Vacancy A', 'Company A', 1000, 2000)])
        output = mock_stdout.getvalue()
        self.assertIn('Вакансия: Vacancy A, Компания: Company A, Зарплата: 1000 - 2000', output)


if __name__ == '__main__':
    unittest.main()
