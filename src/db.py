import psycopg2
import os
from psycopg2 import sql


class Database:
    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
        """Инициализирует соединение с базой данных."""
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.cursor = self.conn.cursor()

    def create_database(self, db_name: str) -> None:
        """
        Создает базу данных, если она не существует.

        Args:
            db_name (str): Имя создаваемой базы данных.
        """
        try:
            conn = psycopg2.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                                    host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'))
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print("База данных успешно создана!")
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            conn.close()

    def create_tables(self) -> None:
        """
        Создает таблицы для работодателей и вакансий.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary_min INT,
                salary_max INT,
                employer_id INT REFERENCES employers(id)
            );
        """)
        self.conn.commit()

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        self.cursor.close()
        self.conn.close()
