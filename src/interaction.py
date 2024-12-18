from typing import List, Tuple


def print_companies_and_vacancies(companies: List[Tuple[str, int]]) -> None:
    """Печатает компании и количество их вакансий."""
    if not companies:
        print("Нет доступных компаний.")
        return
    print("\nКомпании и количество вакансий:")
    for name, count in companies:
        print(f"{name}: {count} вакансий")
    print()


def print_all_vacancies(vacancies: List[Tuple[str, str, int, int]]) -> None:
    """Печатает список всех вакансий."""
    if not vacancies:
        print("Нет доступных вакансий.")
        return
    print("\nСписок всех вакансий:")
    for title, company, salary_min, salary_max in vacancies:
        salary_range = f"{salary_min} - {salary_max}" if salary_min and salary_max else "Не указана"
        print(f"Вакансия: {title}, Компания: {company}, Зарплата: {salary_range}")
    print()


def main_menu(db_manager) -> None:
    """Главное меню для взаимодействия с пользователем."""
    while True:
        print("1 - Получить компании и количество вакансий")
        print("2 - Получить все вакансии")
        print("0 - Выход")

        choice = input("Выберите опцию: ")
        if choice == '1':
            print_companies_and_vacancies(db_manager.get_companies_and_vacancies_count())
        elif choice == '2':
            print_all_vacancies(db_manager.get_all_vacancies())
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
