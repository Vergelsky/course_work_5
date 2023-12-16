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
    bdm = start_work()

    while True:
        response = input("Введите команду:\n"
                         "СК - Список всех Компаний,\n"
                         "СВ - Список всех Вакансий,\n"
                         "СЗ - Средняя Зарплата по всем вакансиям,\n"
                         "ВС - вакансии с зарплатой Выше Средней,\n"
                         "П профа - Поиск вакансий со словом \"профа\" в названии,\n"
                         "В - завершить работу программы.")

        match response.split(" "):
            case ["СК"]:
                bdm.get_companies_and_vacancies_count()
            case ["СВ"]:
                bdm.get_all_vacancies()
            case ["СЗ"]:
                bdm.get_avg_salary()
            case ["ВС"]:
                bdm.get_vacancies_with_higher_salary()
            case ["П"], *name:
                bdm.get_vacancies_with_keyword(name)
            case ["В"]:
                quit()
            case bad_response:
                print(f"Команда {bad_response} не существует, повторите ввод.")
