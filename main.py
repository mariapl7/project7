from api import HHAPI
from db import Database

def main():
    # Здесь вы можете указать интересующие вас компании
    companies_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    # Создайте и настройте базу данных
    db = Database('your_db', 'your_user', 'your_password')
    db.create_tables()

    # Получаем данные о компаниях и их вакансиях
    companies_data = HHAPI.get_companies(companies_ids)
    for company in companies_data:
        db.cursor.execute(
            "INSERT INTO employers (name, vacancies_count) VALUES (%s, %s) RETURNING id",
            (company['name'], company['vacancies_count'])
        )
        employer_id = db.cursor.fetchone()[0]

        vacancies = HHAPI.get_vacancies(company['id'])
        for vacancy in vacancies:
            db.cursor.execute(
                "INSERT INTO vacancies (title, salary_min, salary_max, employer_id) VALUES (%s, %s, %s, %s)",
                (vacancy['name'], vacancy.get('salary', {}).get('from'), vacancy.get('salary', {}).get('to'), employer_id)
            )

    db.conn.commit()
    db.close()

if __name__ == "__main__":
    main()