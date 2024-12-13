class DBManager:
    def __init__(self, database):
        """Инициализирует DBManager с указанной базой данных."""
        self.db = database

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.db.cursor.execute('''
            SELECT e.name, COUNT(v.id) 
            FROM employers e 
            LEFT JOIN vacancies v ON e.id = v.employer_id 
            GROUP BY e.name;
        ''')
        return self.db.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        self.db.cursor.execute('''
            SELECT v.title, e.name, v.salary_min, v.salary_max 
            FROM vacancies v 
            JOIN employers e ON v.employer_id = e.id;
        ''')
        return self.db.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям."""
        self.db.cursor.execute('SELECT AVG(salary_min) FROM vacancies;')
        return self.db.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней."""
        avg_salary = self.get_avg_salary()
        self.db.cursor.execute('''
            SELECT * FROM vacancies WHERE salary_min > %s;
        ''', (avg_salary,))
        return self.db.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержится переданное слово.
        """
        self.db.cursor.execute('''
            SELECT * FROM vacancies WHERE title ILIKE %s;
        ''', (f'%{keyword}%',))
        return self.db.cursor.fetchall()
