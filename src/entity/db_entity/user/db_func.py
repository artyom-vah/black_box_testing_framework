"""
    Функции для работы с сущностью user через БД
"""

from src.entity.db_entity.data_func import (create_set_for_update,
                                            create_values_for_insert)
from src.entity.db_entity.user import table_headers, table_name


class UserDBFunc:
    @staticmethod
    def create(db_client, user_data: dict):
        """Добавляем нового user-а"""
        values_str = create_values_for_insert(user_data)
        insert_sql = f"INSERT INTO {table_name} ({', '.join(table_headers)}) " \
                     f"VALUES ({values_str});"
        db_client.execute_query(insert_sql)

    @staticmethod
    def get_by_id(db_client, user_id: int):
        """Получаем user-а"""
        select_sql = f"SELECT * FROM {table_name} WHERE id = {user_id};"
        return db_client.execute_read_query(select_sql)

    @staticmethod
    def update_by_id(db_client, user_id: int, user_data: dict):
        """Обновляем user-а"""
        set_str = create_set_for_update(user_data)
        update_sql = f"UPDATE {table_name} SET {set_str} WHERE id={user_id};"
        db_client.execute_query(update_sql)

    @staticmethod
    def delete_by_id(db_client, user_id: int):
        delete_sql = f"DELETE FROM {table_name} WHERE id={user_id};"
        db_client.execute_query(delete_sql)

    # TODO написать функцию delete_by_email

    @staticmethod
    def get_id(db_client, email: str):
        select_sql = f"SELECT id FROM {table_name} WHERE email='{email}';"
        return int(db_client.execute_read_query(select_sql)[0][0])


if __name__ == "__main__":
    # для теста
    import os

    import src.config
    from src.clients.db import DBClient
    from src.consts import EnvName

    # CONNECT TO DB
    db_credential = (
        os.getenv(EnvName.DB_NAME),
        os.getenv(EnvName.DB_USER),
        os.getenv(EnvName.DB_PASSWORD),
        os.getenv(EnvName.DB_HOST),
        os.getenv(EnvName.DB_PORT)
    )
    db_client = DBClient()
    db_client.create_connection(*db_credential)

    # CREATE USER
    user_data = {
        "id": 1000,
        "email": "test1000@mail.ru",
        "hashed_password": "demo_hash",
        "full_name": "Петров Петр Сергеевич",
        "income": 10,
        "another_loans": False,
        "birth_date": "1999-01-01",
        "sex": "female",
        "status_document": False,
        "status_face": False
    }
    UserDBFunc.create(db_client, user_data)
    print("create:\n" + str(UserDBFunc.get_by_id(db_client, user_data["id"])))
    # UPDATE USER
    user_update_data = {
        "id": 1000,
        "email": "test1001@mail.ru",
        "hashed_password": "demo_hash1",
        "full_name": "Петров1 Петр1 Сергеевич1",
        "income": 11,
        "another_loans": True,
        "birth_date": "1999-11-11",
        "sex": "male",
        "status_document": True,
        "status_face": True
    }
    UserDBFunc.update_by_id(db_client, user_data["id"], user_update_data)
    print("update:\n" + str(UserDBFunc.get_by_id(db_client, user_data["id"])))
    # DELETE USER
    UserDBFunc.delete_by_id(db_client, user_data["id"])
    assert len(UserDBFunc.get_by_id(db_client, user_data["id"])) == 0, "Error: delete user from table UNSUCCESSFUL!"

    # print(UserDBFunc.get_id(db_client, "test1@mail.ru"))
    db_client.close_connection()
