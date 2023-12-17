from api_hh import VacanciesFromEmployer
from dbmanager import DBManager
import json
import os

employers_file = "employers.json"


def start_work():
    # получаем список избранных компаний
    with open(employers_file, encoding='UTF-8') as file:
        employers_list = json.load(file)[0]

    # создаём базу данных
    dbmanager = DBManager()

    vfe = VacanciesFromEmployer()
    # для каждого работодателя
    for employer in employers_list:
        # загружаем вакансии
        vacancies = vfe.get_vacancies(employers_list[employer])
        vacancies = json.loads(vacancies)
        for vacancy in vacancies['items']:
            # и записываем в бд
            dbmanager.add_note(vacancy)
    # возвращаем бд для дальнейшей работы
    return dbmanager


if __name__ == "__main__":
    dbm = start_work()

    while True:
        response = input("Введите команду:\n"
                         "СК - Список всех Компаний,\n"
                         "СВ - Список всех Вакансий,\n"
                         "СЗ - Средняя Зарплата по всем вакансиям,\n"
                         "ВС - вакансии с зарплатой Выше Средней,\n"
                         "П профа - Поиск вакансий со словом \"профа\" в названии,\n"
                         "В - завершить работу программы.\n")

        match response.split(" "):
            case ["СК"]:
                dbm.print_response(dbm.get_companies_and_vacancies_count())
            case ["СВ"]:
                dbm.print_response(dbm.get_all_vacancies())
            case ["СЗ"]:
                dbm.print_response(dbm.get_avg_salary())
            case ["ВС"]:
                dbm.print_response(dbm.get_vacancies_with_higher_salary())
            case ["П", *name]:
                dbm.print_response(dbm.get_vacancies_with_keyword(name))
            case ["В"]:
                quit()
            case bad_response:
                print(f"Команда {bad_response} не существует, повторите ввод.")
