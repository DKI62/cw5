import sqlite3
import unittest


class DBManager:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employer_id INTEGER,
                name TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                url TEXT,
                FOREIGN KEY (employer_id) REFERENCES employers(id)
            )
        """)
        self.conn.commit()

    def insert_employer(self, employer_data):
        self.cursor.execute(
            "INSERT INTO employers (name) VALUES (?)",
            (employer_data["name"],)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_vacancy(self, employer_id, vacancy_data):
        self.cursor.execute(
            "INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url) VALUES (?, ?, ?, ?, ?)",
            (employer_id, vacancy_data["name"], vacancy_data["salary"]["from"], vacancy_data["salary"]["to"],
             vacancy_data["alternate_url"])
        )
        self.conn.commit()


class TestDBManager(unittest.TestCase):

    def setUp(self):
        # Создаем временную базу данных в памяти
        self.connection = sqlite3.connect(':memory:')
        self.db = DBManager(self.connection)

    def tearDown(self):
        # Закрываем соединение с базой данных
        self.connection.close()

    def test_create_tables(self):
        self.db.create_tables()

        # Проверяем создание таблиц
        self.db.cursor.execute("PRAGMA table_info(employers)")
        employers_info = self.db.cursor.fetchall()
        self.assertGreater(len(employers_info), 0, "Таблица employers не создана")

        self.db.cursor.execute("PRAGMA table_info(vacancies)")
        vacancies_info = self.db.cursor.fetchall()
        self.assertGreater(len(vacancies_info), 0, "Таблица vacancies не создана")

    def test_insert_employer(self):
        self.db.create_tables()
        employer_data = {"name": "Test Employer"}
        employer_id = self.db.insert_employer(employer_data)

        self.assertEqual(employer_id, 1)  # Вставляется первый элемент, id должен быть 1

        # Проверяем вставку
        self.db.cursor.execute("SELECT name FROM employers WHERE id = ?", (employer_id,))
        row = self.db.cursor.fetchone()
        self.assertEqual(row[0], "Test Employer")

    def test_insert_vacancy(self):
        self.db.create_tables()
        employer_data = {"name": "Test Employer"}
        employer_id = self.db.insert_employer(employer_data)

        vacancy_data = {"name": "Test Vacancy", "salary": {"from": 1000, "to": 2000},
                        "alternate_url": "http://example.com"}
        self.db.insert_vacancy(employer_id, vacancy_data)

        # Проверяем вставку
        self.db.cursor.execute("SELECT * FROM vacancies WHERE employer_id = ?", (employer_id,))
        row = self.db.cursor.fetchone()
        self.assertEqual(row[1], employer_id)
        self.assertEqual(row[2], "Test Vacancy")
        self.assertEqual(row[3], 1000)
        self.assertEqual(row[4], 2000)
        self.assertEqual(row[5], "http://example.com")


if __name__ == '__main__':
    unittest.main()
