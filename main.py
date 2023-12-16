from api_hh import VacanciesFromEmployer
import json
import os

employers_file = "employers.json"


def start_work():
    with open(employers_file) as file:
        employers_list = json.load(file)
    print(employers_list)


if __name__ == "main.py":
    start_work()
