"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()
postgres_key = os.getenv("POSTGRESQL_KEY")


class RecieveDataFromCSV:
    """Класс для работы с CSV файлом."""
    @staticmethod
    def get_data_csv(filename: str) -> list:
        """
        Вытаскиваем данные из указанного CSV файла.
        :param filename: Имя нужного файла.
        :return: Список преобразованных данных.
        """
        all_data = []
        with open(filename, encoding="utf-8") as file:
            full_data = csv.DictReader(file)
            for data in full_data:
                all_data.append(data)
        return all_data


data_reciever = RecieveDataFromCSV()
customers = data_reciever.get_data_csv("north_data/customers_data.csv")
employees = data_reciever.get_data_csv("north_data/employees_data.csv")

employee_id = 1
for employee in employees:
    employee["employee_id"] = employee_id
    employee_id += 1

orders = data_reciever.get_data_csv("north_data/orders_data.csv")

conn = psycopg2.connect(
    host="localhost", database="north", user="postgres", password="8953", port="5432"
)

try:
    with conn:
        with conn.cursor() as cur:
            conn.autocommit = True
            for customer in range(len(customers)):
                cur.execute(
                    "INSERT INTO customers_data VALUES (%s, %s, %s)",
                    (
                        customers[customer]["customer_id"],
                        customers[customer]["company_name"],
                        customers[customer]["contact_name"],
                    ),
                )

            for employee in range(len(employees)):
                cur.execute(
                    "INSERT INTO employees_data VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        employees[employee]["employee_id"],
                        employees[employee]["first_name"],
                        employees[employee]["last_name"],
                        employees[employee]["title"],
                        employees[employee]["birth_date"],
                        employees[employee]["notes"],
                    ),
                )

            for order in range(len(orders)):
                cur.execute(
                    "INSERT INTO orders_data VALUES (%s, %s, %s, %s, %s)",
                    (
                        orders[order]["order_id"],
                        orders[order]["customer_id"],
                        orders[order]["employee_id"],
                        orders[order]["order_date"],
                        orders[order]["ship_city"],
                    ),
                )

finally:
    cur.close()
    conn.close()
