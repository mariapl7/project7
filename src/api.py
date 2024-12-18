import requests
from typing import List, Dict


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_companies(companies_ids: List[str]) -> List[Dict]:
        """Получает информацию о компаниях по их идентификаторам."""
        companies = []
        for company_id in companies_ids:
            response = requests.get(f"{HHAPI.BASE_URL}/employers/{company_id}")
            if response.status_code == 200:
                companies.append(response.json())
        return companies

    @staticmethod
    def get_vacancies(company_id: str) -> List[Dict]:
        """Получает список вакансий для конкретной компании."""
        response = requests.get(f"{HHAPI.BASE_URL}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            return response.json().get('items', [])
        return []
