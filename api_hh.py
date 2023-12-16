import requests


class VacanciesFromEmployer():
    qty_vacancies = 20
    api_url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, employer_id):
        """
        Загружает с hh.ru и возвращает список вакансий работодателя в json
        """
        response = requests.get(self.api_url, params={"per_page": self.qty_vacancies, "employer_id": employer_id})
