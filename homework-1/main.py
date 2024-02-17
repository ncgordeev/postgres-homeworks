"""Скрипт для заполнения данными таблиц в БД Postgres."""
import os
import psycopg2
import csv


DB_USER = os.environ.get("PSQL_USER")
DB_PASS = os.environ.get("PSQL_PASS")

conn_params = {
    "host": "localhost",
    "database": "north",
    "user": DB_USER,
    "password": DB_PASS,
}


def fill_tables(title):
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                with open(f"north_data/{title}_data.csv", encoding="utf-8") as file:
                    raw_data = csv.DictReader(file)
                    data = [[v for v in d.values()] for d in raw_data]
                    values_quantity = ("%s, " * len(data[0])).rstrip(", ")
                    for values in data:
                        cur.execute(f"INSERT INTO {title} VALUES ({values_quantity})", (values))
                    print("Данные добавлены в таблицу")
    finally:
        conn.close()
    print("Соединение с базой закрыто\n")


if __name__ == "__main__":
    table_titles = ["employees", "customers", "orders"]

    for title in table_titles:
        fill_tables(title)
