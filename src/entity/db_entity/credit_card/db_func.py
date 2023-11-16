"""
    Функции для работы с сущностью credit_card через БД
"""

from src.entity.db_entity.credit_card import table_headers, table_name
from src.entity.db_entity.data_func import (create_set_for_update,
                                            create_values_for_insert)


class CreditCardDBFunc:
    @staticmethod
    def new(db_client, credit_card_data: dict):
        """Добавляем новую credit_card"""
        values_str = create_values_for_insert(credit_card_data)
        insert_sql = f"INSERT INTO {table_name} ({', '.join(table_headers)}) " \
                     f"VALUES ({values_str});"
        db_client.execute_query(insert_sql)

    @staticmethod
    def get_by_id(db_client, credit_card_id: int):
        """Получаем credit_card по id"""
        select_sql = f"SELECT * FROM {table_name} WHERE id = {credit_card_id};"
        return db_client.execute_read_query(select_sql)

    @staticmethod
    def get_by_user_id(db_client, user_id: int):
        """Получаем credit_card по id"""
        select_sql = f"SELECT * FROM {table_name} WHERE user_id = {user_id};"
        return db_client.execute_read_query(select_sql)

    @staticmethod
    def update_by_id(db_client, credit_card_id: int, credit_card_data: dict):
        """Обновляем credit_card"""
        set_str = create_set_for_update(credit_card_data)
        update_sql = f"UPDATE {table_name} SET {set_str} WHERE id={credit_card_id};"
        db_client.execute_query(update_sql)

    @staticmethod
    def delete_by_id(db_client, credit_card_id: int):
        """Удаляем credit_card по id"""
        delete_sql = f"DELETE FROM {table_name} WHERE id={credit_card_id};"
        db_client.execute_query(delete_sql)

    @staticmethod
    def delete_by_user_id(db_client, user_id: int):
        """Удаляем credit_card по user_id"""
        delete_sql = f"DELETE FROM {table_name} WHERE user_id={user_id};"
        db_client.execute_query(delete_sql)

    @staticmethod
    def get_ids_by_user_id(db_client, user_id: int) -> list:
        """Получаем ВСЕ id-шиники credit-card для User-а"""
        select_sql = f"SELECT id FROM {table_name} WHERE user_id='{user_id}';"
        result = db_client.execute_read_query(select_sql)
        return [x[0] for x in result]


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

    # # CREATE CERDIT_CARD
    credit_card_data = {
        "id": 1000,
        "user_id": 1,
        "limit": 100,
        "balance": 10,
        "active": True,
        "exp_date": "1999-01-01",
    }
    # CreditCardDBFunc.new(db_client, credit_card_data)
    # print("create:\n" + str(CreditCardDBFunc.get_by_id(db_client, credit_card_data["id"])))
    print("get_by_user_id:\n" + str(CreditCardDBFunc.get_by_user_id(db_client, credit_card_data["user_id"])))
    # UPDATE CREDIT_CARD
    credit_card_update_data = {
        # ОПЕРАТОРЫ SQL ПРИХОДИТСЯ ЭКРАНИРОВАТЬ!!!
        '"limit"': 101,
        "balance": 101,
        "active": False,
        "exp_date": "2000-01-01",
    }
    CreditCardDBFunc.update_by_id(db_client, credit_card_data["id"], credit_card_update_data)
    print("update:\n" + str(CreditCardDBFunc.get_by_id(db_client, credit_card_data["id"])))
    # GET ALL CREDIT_CARD IDS FOR USER
    print("get ids by user_id:\n" + str(CreditCardDBFunc.get_ids_by_user_id(db_client, credit_card_data["user_id"])))

    # DELETE CREDIT_CARD
    CreditCardDBFunc.delete_by_id(db_client, credit_card_data["id"])
    assert len(CreditCardDBFunc.get_by_id(db_client,
                                          credit_card_data["id"])) == 0, "Error: delete user from table UNSUCCESSFUL!"
    # DELETE ALL CREDIT_CARD FOR USER
    CreditCardDBFunc.delete_by_user_id(db_client, credit_card_data["user_id"])
    assert len(CreditCardDBFunc.get_by_user_id(db_client, credit_card_data[
        "user_id"])) == 0, "Error: delete user from table UNSUCCESSFUL!"

    db_client.close_connection()
