import psycopg2
import json


class DBManager:

    def __init__(self):
        """
        Создаём структуру бд
        """
        self.execute_to_db("CREATE TABLE IF NOT EXISTS employeers_and_vacancies"
                           "("
                           "vacancy_id INTEGER PRIMARY KEY,"
                           "vacancy_name VARCHAR(255),"
                           "salary INTEGER,"
                           "url VARCHAR(255),"
                           "employeer VARCHAR(255)"
                           ");")

    def execute_to_db(self, text, *args):
        """
        Отправляет команду в бд
        :param text: текст команды
        :param args: кортеж с переменными для подстановки в текст команды
        :return:
        """
        db = psycopg2.connect(host='localhost',
                              database='postgres',
                              user='postgres',
                              password='5455')

        try:
            with db:
                with db.cursor() as cursor:
                    # id вакансии, название вакансии, зарплата, ссылка на вакансию, название компании
                    cursor.execute(text, *args)
                    try:
                        res = cursor.fetchall()
                    except: res = None

        finally:
            db.close()
        return res

    def add_note(self, vacancy):
        """
        Принимает словарь вакансии с hh.ru и добавляет в бд.
        :vacancy: вакансия в виде словаря
        """
        id, name, url, emp = (vacancy['id'],
                              vacancy['name'],
                              vacancy['url'],
                              vacancy['employer']['name'])
        # если зарплата указана - берем нижний порог, если его нет, то верхний
        # если не указана - сохраняем None
        if vacancy['salary']:
            if vacancy['salary']['from']:
                sal = vacancy['salary']['from']
            else:
                sal = vacancy['salary']['to']
        else:
            sal = None

        self.execute_to_db("INSERT INTO employeers_and_vacancies VALUES"
                           "(%s, %s, %s, %s, %s)"
                           "ON CONFLICT (vacancy_id) DO NOTHING",
                           (id, name, sal, url, emp))

    def print_response(self, response):
        for line in response:
            print(*line)

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        return self.execute_to_db("SELECT employeer, COUNT(*) FROM employeers_and_vacancies GROUP BY employeer")

    def get_all_vacancies(self):
        """
         Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword(self, name):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        pass
