import unittest
from unittest.mock import MagicMock, patch
from src.interaction import main_menu


class TestInteraction(unittest.TestCase):

    def test_main_menu(self):
        mock_db_manager = MagicMock()
        mock_db_manager.get_companies_and_vacancies_count.return_value = [('Company A', 5)]
        mock_db_manager.get_all_vacancies.return_value = [('Vacancy A', 'Company A', 1000, 2000)]

        # Здесь можно заменить input на заманчивый тестовый вход
        # Например, вы можете заменить input для симуляции ввода
        with patch('builtins.input', side_effect=['1', '0']):
            main_menu(mock_db_manager)

        # Проверяем, вызывается ли метод для получения компаний и количества вакансий
        mock_db_manager.get_companies_and_vacancies_count.assert_called_once()


if __name__ == '__main__':
    unittest.main()
