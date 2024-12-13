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
        self.mock_cursor.execute.assert_any_call()

    def test_close(self):
        self.db.close()
        self.mock_cursor.close.assert_called_once()
        self.mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
