import requests


class HHAPI:
    BASE_URL = 'https://api.hh.ru'

    @staticmethod
    def get_companies(companies):
        """Получает данные о компаниях по их ID."""
        companies_data = []
        for company in companies:
            response = requests.get(f"{HHAPI.BASE_URL}/employers/{company}")
            if response.status_code == 200:
                companies_data.append(response.json())
        return companies_data

    @staticmethod
    def get_vacancies(company_id):
        """Получает вакансии для определенной компании по ее ID."""
        vacancies = []
        response = requests.get(f"{HHAPI.BASE_URL}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
        return vacancies
