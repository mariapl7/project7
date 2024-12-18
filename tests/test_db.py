import unittest
from unittest.mock import patch, MagicMock
from src.db import Database


class TestDatabase(unittest.TestCase):
    """Тесты для класса Database."""

    @patch('src.db.psycopg2.connect')
    def setUp(self, mock_connect):
        """Настройка тестового окружения для класса Database."""
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.db = Database('test_db', 'user', 'pass', 'localhost', '5432')

    def test_create_tables(self):
        """Тестирует создание таблиц в базе данных."""
        self.db.create_tables()
        self.mock_conn.cursor.return_value.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS employers (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL);"
        )
        self.mock_conn.cursor.return_value.execute.assert_any_call(
            "CREATE TABLE IF NOT EXISTS vacancies "
            "("
            "id SERIAL PRIMARY KEY, "
            "title VARCHAR(255) NOT NULL, "
            "salary_min INT, salary_max INT, "
            "employer_id INT REFERENCES employers(id));"
        )

    def test_close(self):
        """Тестирует закрытие соединения с базой данных."""
        self.db.close()
        self.mock_conn.cursor().close.assert_called_once()
        self.mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
