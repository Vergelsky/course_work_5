from api_hh import VacanciesFromEmployer
import json
import os

employers_file = "employers.json"


def start_work():
    #получаем список избранных компаний
    with open(employers_file, encoding='UTF-8') as file:
        employers_list = json.load(file)

    #создаём базу данных
    bdm = BDManager()

    vfe = VacanciesFromEmployer()

    #для каждого работодателя
    for employer in employers_list:
        #загружаем вакансии
        vacancies = vfe.get_vacancies(employer)
        for vacancy in vacancies:
            #и записываем в бд
            bdm.add_note(vacancy)
    #возвращаем бд для дальнейшей работы
    return bdm

if __name__ == "__main__":
    bdm = start_work()

    while True:
        responce = input("Введите команду:\n"
                         "СК - Список всех Компаний,\n"
                         "СВ - Список всех Вакансий,\n"
                         "СЗ - Средняя Зарплата по всем вакансиям,\n"
                         "ВС - вакансии с зарплатой Выше Средней,\n"
                         "П профа - Поиск вакансий со словом \"профа\" в названии,\n"
                         "В - завершить работу программы.")

        match responce.split(" "):
            case ["СК"]:
                bdm.get_companies_and_vacancies_count()
            case ["СВ"]:
                bdm.get_all_vacancies()
            case ["СЗ"]:
                bdm.get_avg_salary()
            case ["ВС"]:
                bdm.get_rich_vacancies()
            case ["П"], *name:
                bdm.search_in_vacancies(name)
            case ["В"]:
                quit()
            case bad_response:
                print(f"Команда {bad_response} не существует, повторите ввод.")