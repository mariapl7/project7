import psycopg2
from typing import Optional


class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """Создает подключение к базе данных PostgreSQL."""
        try:
            self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise Exception(f"Ошибка подключения к базе данных: {e}")

    def create_tables(self) -> None:
        """Создает таблицы в базе данных, если они не существуют."""
        try:
            create_employers_table = """
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    vacancies_count INTEGER
                );
            """
            create_vacancies_table = """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    employer_id INTEGER,
                    FOREIGN KEY (employer_id) REFERENCES employers (id)
                );
            """

            self.cursor.execute(create_employers_table)
            self.cursor.execute(create_vacancies_table)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Ошибка при создании таблиц: {e}")

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise Exception(f"Ошибка при закрытии соединения: {e}")
