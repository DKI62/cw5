import psycopg2
import os
from typing import Dict


class DBManager:
    def __init__(self) -> None:
        dbname = os.getenv("DB_NAME", "cw5")
        user = os.getenv("DB_USER", "admin")
        password = os.getenv("DB_PASSWORD", "12345")
        host = os.getenv("DB_HOST", "localhost")
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()

    def create_tables(self) -> None:
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(id),
                    name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    url TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()

    def insert_employer(self, employer_data: Dict) -> int:
        """
        Вставляет данные о работодателе в базу данных.

        :param employer_data: Словарь с данными о работодателе.
        :return: ID работодателя.
        """
        name = employer_data["name"]

        self.cursor.execute("""
            INSERT INTO employers (name) VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
        """, (name,))

        result = self.cursor.fetchone()
        if result:
            return result[0]

        # В случае, если работодателя уже нет в базе, получаем его ID
        self.cursor.execute("""
            SELECT id FROM employers WHERE name = %s
        """, (name,))
        return self.cursor.fetchone()[0]

    def insert_vacancy(self, employer_id: str, vacancy_data: Dict) -> None:
        """
        Вставляет данные о вакансии в базу данных.

        :param employer_id: ID работодателя.
        :param vacancy_data: Словарь с данными о вакансии.
        """
        salary = vacancy_data.get("salary", {})
        salary_from = salary.get("from") if salary else None
        salary_to = salary.get("to") if salary else None

        self.cursor.execute("""
            INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url)
            VALUES (%s, %s, %s, %s, %s)
        """, (employer_id, vacancy_data["name"], salary_from, salary_to, vacancy_data.get("alternate_url")))

        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        self.cursor.execute("""
            SELECT employers.name, COUNT(vacancies.id)
            FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.name
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cursor.execute("""
            SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.id
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        self.cursor.execute("""
            SELECT AVG(salary_from) AS avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.id
            WHERE vacancies.salary_from > %s
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

        :param keyword: Ключевое слово для поиска.
        """
        self.cursor.execute("""
            SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.id
            WHERE vacancies.name ILIKE %s
        """, (f"%{keyword}%",))
        return self.cursor.fetchall()

    def close(self) -> None:
        """
        Закрывает соединение и курсор.
        """
        self.cursor.close()
        self.conn.close()
