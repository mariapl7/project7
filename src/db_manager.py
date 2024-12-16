from typing import List, Tuple, Optional
import sqlite3
import os
from src.db import Database


def create_database(db_name: str) -> None:
    """Создает базу данных и таблицы, если они не существуют."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            employer_id INTEGER,
            FOREIGN KEY (employer_id) REFERENCES employers (id) ON DELETE CASCADE
        );
    ''')
    connection.commit()
    connection.close()


class DBManager:
    def __init__(self, database: 'Database') -> None:
        """Инициализирует DBManager с указанной базой данных."""
        self.db = database

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.db.cursor.execute('''
            SELECT e.name, COUNT(v.id) 
            FROM employers e 
            LEFT JOIN vacancies v ON e.id = v.employer_id 
            GROUP BY e.name;
        ''')
        return self.db.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int]]]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        self.db.cursor.execute('''
            SELECT v.title, e.name, v.salary_min, v.salary_max 
            FROM vacancies v 
            JOIN employers e ON v.employer_id = e.id;
        ''')
        return self.db.cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Получает среднюю зарплату по всем вакансиям."""
        self.db.cursor.execute('SELECT AVG(salary_min) FROM vacancies;')
        return self.db.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[int, str, Optional[int], Optional[int]]]:
        """Получает список всех вакансий, у которых зарплата выше средней."""
        avg_salary = self.get_avg_salary()
        self.db.cursor.execute('''
            SELECT * FROM vacancies WHERE salary_min > ?;
        ''', (avg_salary,))
        return self.db.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[int, str, Optional[int], Optional[int]]]:
        """Получает список всех вакансий, в названии которых содержится переданное слово."""
        self.db.cursor.execute('''
            SELECT * FROM vacancies WHERE title LIKE ?;
        ''', (f'%{keyword}%',))
        return self.db.cursor.fetchall()


if __name__ == "__main__":
    DB_NAME = os.getenv('DB_NAME', 'my_database.db')  # Имя базы данных из переменных окружения
    create_database(DB_NAME)  # Создание базы данных и таблиц

    connection = sqlite3.connect(DB_NAME)  # Подключение к базе данных
    connection.row_factory = sqlite3.Row  # Чтобы могли обращаться к столбцам по имени
    db_manager = DBManager(connection)
