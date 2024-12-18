from src.db import Database
from typing import List, Tuple


class DBManager:
    def __init__(self, db: Database):
        """Инициализирует менеджер базы данных."""
        self.db = db

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список компаний и количество их вакансий."""
        self.db.cursor.execute("""
            SELECT e.name, COUNT(v.id)
            FROM employers e
            LEFT JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.id;
        """)
        return self.db.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int]]:
        """Получает список всех вакансий с указанием названия компании."""
        self.db.cursor.execute("""
            SELECT title, e.name, salary_min, salary_max 
            FROM vacancies v JOIN employers e ON v.employer_id = e.id;
        """)
        return self.db.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по всем вакансиям."""
        self.db.cursor.execute("SELECT AVG(salary_min + salary_max) / 2 FROM vacancies;")
        return self.db.cursor.fetchone()[0]

    def get_high_salary_vacancies(self) -> List[Tuple[str, str, int, int]]:
        """Получает список вакансий с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        self.db.cursor.execute("""
            SELECT title, e.name, salary_min, salary_max
            FROM vacancies v JOIN employers e ON v.employer_id = e.id
            WHERE (salary_min + salary_max) / 2 > %s;
        """, (avg_salary,))
        return self.db.cursor.fetchall()

    def get_vacancies_by_keyword(self, keyword: str) -> List[Tuple[str, str]]:
        """Получает список вакансий по ключевому слову в названии."""
        self.db.cursor.execute("""
            SELECT title, e.name, salary_min, salary_max
            FROM vacancies v JOIN employers e ON v.employer_id = e.id
            WHERE title LIKE %s;
        """, (f'%{keyword}%',))
        return self.db.cursor.fetchall()

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self.db.close()
