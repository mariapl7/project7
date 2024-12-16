import requests
from typing import List, Dict, Any


class HHAPI:
    BASE_URL = 'https://api.hh.ru'

    @staticmethod
    def get_companies(companies: List[int]) -> List[Dict[str, Any]]:
        """Получает данные о компаниях по их ID."""
        companies_data: List[Dict[str, Any]] = []
        for company in companies:
            response = requests.get(f"{HHAPI.BASE_URL}/employers/{company}")
            if response.status_code == 200:
                companies_data.append(response.json())
        return companies_data

    @staticmethod
    def get_vacancies(company_id: int) -> List[Dict[str, Any]]:
        """Получает вакансии для определенной компании по ее ID."""
        vacancies: List[Dict[str, Any]] = []
        response = requests.get(f"{HHAPI.BASE_URL}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
        return vacancies
