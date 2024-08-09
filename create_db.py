import psycopg2
from psycopg2 import sql

def create_database():
    conn = psycopg2.connect(dbname='postgres', user='admin', password='12345', host='localhost')
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('cw5')))
        print("Database created successfully.")
        db_created = True
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists.")
        db_created = False

    conn.close()
    return db_created

if __name__ == "__main__":
    create_database()
