import requests
import os
from abc import ABC, abstractmethod


class JobSitesAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(JobSitesAPI):
    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self, count_page=5):
        params = {
            'text': self.keyword,  # Ключевое слово запроса
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 20  # Кол-во вакансий на 1 странице
        }
        data = []
        try:
            while params["page"] < count_page:
                response = requests.get('https://api.hh.ru/vacancies', params=params)
                if response.status_code == 200:
                    print(f"Парсинг {params['page'] + 1} страницы")
                    data.extend(response.json()["items"])
                    params["page"] += 1
                else:
                    print(f'HeadHunter response: Error {response.status_code}')
                    return None
            return data
        except (requests.exceptions.HTTPError, requests.ConnectionError):
            print('HeadHunter response: Connection failed')
            return None


class SuperJobAPI(JobSitesAPI):
    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self, count_page=5):
        api_key: str = os.getenv('SJ_API_KEY')
        headers = {"X-Api-App-Id": api_key}
        params = {
            "keyword": self.keyword,
            "page": 0,
            "count": 20
        }

        data = []
        try:
            while params["page"] < count_page:
                response = requests.get("https://api.superjob.ru/2.0/vacancies/",
                                        headers=headers, params=params,)
                if response.status_code == 200:
                    print(f"Парсинг {params['page'] + 1} страницы")
                    data.extend(response.json()["objects"])
                    params["page"] += 1
                else:
                    print(f'SuperJob response: Error {response.status_code}')
                    return None
            return data
        except (requests.exceptions.HTTPError, requests.ConnectionError):
            print('SuperJob response: Connection failed')
            return None
