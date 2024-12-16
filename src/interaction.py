from typing import Union
from src.db_manager import DBManager


def main_menu(db_manager: 'DBManager') -> None:
    """Главное меню для взаимодействия с пользователем."""
    while True:
        print("1 - Получить компании и количество вакансий")
        print("2 - Получить все вакансии")
        print("3 - Получить среднюю зарплату")
        print("4 - Получить вакансии с зарплатой выше средней")
        print("5 - Получить вакансии по ключевому слову")
        print("0 - Выход")

        choice: str = input("Выберите опцию: ")
        if choice == '1':
            print(db_manager.get_companies_and_vacancies_count())
        elif choice == '2':
            print(db_manager.get_all_vacancies())
        elif choice == '3':
            print(db_manager.get_avg_salary())
        elif choice == '4':
            print(db_manager.get_vacancies_with_higher_salary())
        elif choice == '5':
            keyword: str = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))
        elif choice == '0':
            break
