import unittest
from unittest.mock import MagicMock, patch
from src.db import Database


class TestDatabase(unittest.TestCase):
    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.db = Database(dbname='test_db', user='test_user', password='test_password')

    def test_create_tables(self):
        self.db.create_tables()

        create_employers_sql = """
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                vacancies_count INTEGER
            );
        """.strip()  # Обратите внимание на совпадения с методом create_tables

        create_vacancies_sql = """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary_min INTEGER,
                salary_max INTEGER,
                employer_id INTEGER,
                FOREIGN KEY (employer_id) REFERENCES employers (id)
            );
        """.strip()  # Обратите внимание на совпадения с методом create_tables

        # Проверка всех вызовов execute на mock_cursor
        self.mock_cursor.execute.assert_any_call(create_employers_sql)
        self.mock_cursor.execute.assert_any_call(create_vacancies_sql)

    def test_close(self):
        self.db.close()
        self.mock_cursor.close.assert_called_once()
        self.mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
