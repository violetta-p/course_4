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

    def get_vacancies(self):
        params = {
            'text': self.keyword,  # Ключевое слово запроса
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 2  # Кол-во вакансий на 1 странице
        }
        try:
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f'HeadHunter response: Error {response.status_code}')
                return None
        except (requests.exceptions.HTTPError, requests.ConnectionError):
            print('HeadHunter response: Connection failed')
            return None


class SuperJobAPI(JobSitesAPI):
    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self):
        api_key: str = os.getenv('SJ_API_KEY')
        headers = {"X-Api-App-Id": api_key}
        params = {
            "keyword": self.keyword,
            "page": 0,
            "count": 2
        }
        try:
            response = requests.get("https://api.superjob.ru/2.0/vacancies/",
                                    headers=headers, params=params,)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f'SuperJob response: Error {response.status_code}')
                return None
        except (requests.exceptions.HTTPError, requests.ConnectionError):
            print('SuperJob response: Connection failed')
            return None
