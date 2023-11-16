"""
    Клиент для работы с DB Postgress
"""

import psycopg2
from psycopg2 import DatabaseError, OperationalError


class DBClient:
    """Клиент для работы с БД"""

    def __init__(self):
        self.connection = None

    def create_connection(self, db_name, db_user, db_password, db_host, db_port: str):
        """Создаем connection к Postgress"""
        try:
            # пытаемся подключиться к бд
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=int(db_port),
            )
            # настраиваем connection
            self.connection.set_session(readonly=False, autocommit=True)
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            raise DatabaseError(f"The error on create_connection to PostgreSQL DB") from e

    def close_connection(self):
        """Закрываем connection к Postgress"""
        try:
            self.connection.close()
            print("Close connection to PostgreSQL DB successful")
        except Exception as e:
            raise DatabaseError(f"The error on close_connection to PostgreSQL DB") from e

    def execute_read_query(self, query):
        """Послылаем SQL запрос и ждем ответ от БД"""
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            raise DatabaseError(f"The error on execute_read_query to PostgreSQL DB") from e

    def execute_query(self, query):
        """Послылаем SQL запрос и НЕ ждем ответ от БД"""
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
        except Exception as e:
            raise DatabaseError(f"The error on execute_query to PostgreSQL DB") from e


if __name__ == "__main__":
    # для теста
    import os

    import src.config

    # connect to db
    db_credential = (
        os.getenv("DB_NAME"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT")
    )
    db_client = DBClient()
    db_client.create_connection(*db_credential)

    # simle select
    USERS_TABLE_NAME = "public.user"
    USER_ID = 1000
    select_users_sql = f"select * from {USERS_TABLE_NAME}"
    result = db_client.execute_read_query(select_users_sql)
    print(result[:2])
    # insert new row
    USERS_TABLE_HEADERS = ["id", "email", "hashed_password", "full_name", "income", "another_loans", "birth_date",
                           "sex", "status_document", "status_face"]
    insert_user_sql = f"INSERT INTO {USERS_TABLE_NAME} ({', '.join(USERS_TABLE_HEADERS)}) " \
                      f"VALUES ({USER_ID}, 'del@mail.ru', 'del_hash', 'del_fullname', 1, false, " \
                      "'2000-01-01', 'male', false, false);"
    db_client.execute_query(insert_user_sql)
    # delete row
    delete_user_sql = f"DELETE FROM {USERS_TABLE_NAME} WHERE id={USER_ID};"
    db_client.execute_query(delete_user_sql)

    db_client.close_connection()
