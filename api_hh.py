import requests


class VacanciesFromEmployer():
    max_qty_vacancies = 100
    api_url = "https://api.hh.ru/vacancies/"

    def load_vacancies(self, employer_id):
        """
        Загружает с hh.ru и возвращает список вакансий работодателя в json
        """
        response = requests.get(self.api_url, params={"per_page": self.max_qty_vacancies, "employer_id": employer_id})
