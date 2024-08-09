import requests
from typing import List, Dict

class HHVacanciesAPI:
    def __init__(self) -> None:
        """
        Инициализация клиента API HH.ru.
        """
        self.base_url = "https://api.hh.ru/"

    def get_employers(self, employer_ids: List[str]) -> List[Dict]:
        """
        Получает информацию о работодателях по их ID.

        :param employer_ids: Список ID работодателей.
        :return: Список словарей с данными о работодателях.
        """
        employers = []
        for employer_id in employer_ids:
            url = f"{self.base_url}employers/{employer_id}"
            response = requests.get(url)
            if response.status_code == 404:
                print(f"Employer with ID {employer_id} not found.")
                continue
            response.raise_for_status()
            employers.append(response.json())
        return employers

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """
        Получает вакансии для заданного ID работодателя.

        :param employer_id: ID работодателя.
        :return: Список словарей с данными о вакансиях.
        """
        url = f"{self.base_url}vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": 100,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["items"]
