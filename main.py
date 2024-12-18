from dotenv import load_dotenv
from src.api import HHAPI
from src.db import Database
from src.db_manager import DBManager
from src.interaction import main_menu
import logging
import os

# Загрузка переменных окружения из .env
load_dotenv()

# Установка конфигурации логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Основная функция программы, выполняющая настройку базы данных и запуск меню.
    """
    # Получаем параметры подключения из переменных окружения
    db_name = os.getenv('DB_NAME', 'test_db')
    db_user = os.getenv('DB_USER', 'test_user')
    db_password = os.getenv('DB_PASSWORD', 'test_password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')

    # Создание и настройка базы данных
    db = Database(db_name, db_user, db_password, db_host, db_port)
    db.create_database(db_name)  # Вызов для создания БД
    db.create_tables()

    companies_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    try:
        # Получаем данные о компаниях и их вакансиях
        companies_data = HHAPI.get_companies(companies_ids)

        for company in companies_data:
            logging.info(f"Вставка данных о компании: {company['name']}")
            db.cursor.execute(
                "INSERT INTO employers (name) VALUES (%s) RETURNING id",
                (company['name'],)
            )
            employer_id = db.cursor.fetchone()[0]

            vacancies = HHAPI.get_vacancies(company['id'])
            for vacancy in vacancies:
                salary_min = vacancy.get('salary', {}).get('from', None)
                salary_max = vacancy.get('salary', {}).get('to', None)
                logging.info(f"Добавление вакансии: {vacancy['name']} для компании: {company['name']}")
                db.cursor.execute(
                    "INSERT INTO vacancies (title, salary_min, salary_max, employer_id) VALUES (%s, %s, %s, %s)",
                    (vacancy['name'], salary_min, salary_max, employer_id)
                )
        db.conn.commit()
        logging.info("Все данные успешно вставлены в базу данных.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        db.conn.rollback()
    finally:
        db.close()
        logging.info("Соединение с базой данных закрыто.")

    # Запускаем главное меню
    main_menu(DBManager(db))


if __name__ == "__main__":
    main()
