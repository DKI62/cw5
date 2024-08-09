from src.db import DBManager
from src.api import HHVacanciesAPI

def user_interface():
    """
    Функция взаимодействия с пользователем. Предоставляет меню для выбора различных операций и взаимодействия с БД.
    """
    # Инициализация API клиента и менеджера БД
    api = HHVacanciesAPI()
    db = DBManager()

    # Основное меню
    while True:
        print("\nВыберите действие:")
        print("1 - Показать список всех компаний и кол-во вакансий у каждой компании")
        print("2 - Показать список всех вакансий")
        print("3 - Показать среднюю зарплату по вакансиям")
        print("4 - Показать вакансии с зарплатой выше средней")
        print("5 - Найти вакансии по ключевому слову")
        print("0 - Выйти")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            companies = db.get_companies_and_vacancies_count()
            print("\nСписок компаний и количество вакансий:")
            for company, vacancies_count in companies:
                print(f"Компания: {company}, Количество вакансий: {vacancies_count}")
        elif choice == "2":
            vacancies = db.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for company, name, salary_from, salary_to, url in vacancies:
                salary_info = f"Зарплата: от {salary_from} до {salary_to} руб." if salary_from and salary_to else "Зарплата не указана"
                print(f"Компания: {company}, Вакансия: {name}, {salary_info}, Ссылка: {url}")
        elif choice == "3":
            avg_salary = db.get_avg_salary()
            if avg_salary:
                print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f} руб.")
            else:
                print("\nЗарплата в вакансиях не указана.")
        elif choice == "4":
            vacancies = db.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for company, name, salary_from, salary_to, url in vacancies:
                salary_info = f"Зарплата: от {salary_from} до {salary_to} руб." if salary_from and salary_to else "Зарплата не указана"
                print(f"Компания: {company}, Вакансия: {name}, {salary_info}, Ссылка: {url}")
        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска вакансий: ").strip()
            vacancies = db.get_vacancies_with_keyword(keyword)
            if vacancies:
                print(f"\nВакансии, содержащие '{keyword}':")
                for company, name, salary_from, salary_to, url in vacancies:
                    salary_info = f"Зарплата: от {salary_from} до {salary_to} руб." if salary_from and salary_to else "Зарплата не указана"
                    print(f"Компания: {company}, Вакансия: {name}, {salary_info}, Ссылка: {url}")
            else:
                print(f"\nВакансий, содержащих '{keyword}', не найдено.")
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

    # Закрытие соединения с БД
    db.close()

if __name__ == "__main__":
    user_interface()
