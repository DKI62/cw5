from src.api import HHVacanciesAPI
from src.db import DBManager
from create_db import create_database
from src.user_interface import user_interface


def main():
    # Создание базы данных (если она еще не существует)
    create_database()

    # Список ID работодателей
    employer_ids = ["933344", "10997442", "4935440", "10889402", "3754394", "2733062", "4304968", "664709", "2324020",
                    "3244995"]

    # Создание API клиента и менеджера БД
    api = HHVacanciesAPI()
    db = DBManager()

    # Создание таблиц в БД
    db.create_tables()

    # Получение данных о работодателях и их вакансиях
    employers = api.get_employers(employer_ids)
    for employer in employers:
        employer_id = db.insert_employer(employer)
        vacancies = api.get_vacancies(employer["id"])
        for vacancy in vacancies:
            db.insert_vacancy(employer_id, vacancy)

    # Запуск пользовательского интерфейса
    user_interface()

    # Закрытие соединения с БД
    db.close()


if __name__ == "__main__":
    main()
