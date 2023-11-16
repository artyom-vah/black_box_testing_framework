from dataclasses import dataclass

from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from src.entity.api_entity.user.data_func import UserDataFunc
from src.entity.db_entity.user.db_func import UserDBFunc
from src.entity.high_level.credit_card import CreditCard
from src.entity.high_level.data_func import Updatable


@dataclass
class UserCredentials(Updatable):
    """Credential данные пользователя"""
    email: str = None
    password: str = None
    auth_header: str = None


@dataclass
class UserData(Updatable):
    """Основные данные пользователя"""
    id: int = None
    full_name: str = None
    income: int = None
    another_loans: bool = None
    birth_date: str = None
    sex: str = None
    email: str = None
    status_document: bool = None
    status_face: bool = None


class User:
    def __init__(self, db_client, email, password):
        self.data = UserData()
        self.credit_card: CreditCard = None
        self.credentials = UserCredentials(email=email, password=password)
        self.db_client = db_client

    def register(self):
        """Регистрируем user-а"""
        UserApiFuncPositive.register(self._get_credential_body())
        self.data.id = UserDBFunc.get_id(self.db_client, self.credentials.email)

    def auth(self):
        """Авторизуем user-а"""
        self.credentials.auth_header = UserDataFunc.get_auth_header(self._get_credential_form())
        self._update_data_from_server()

    def update(self, user_body: dict):
        """Обновляем текущего user-а (обновляем данные на сервере)"""
        UserApiFuncPositive.update(user_body, headers=self.credentials.auth_header)
        self._update_data_from_server()

    def add_document_photo(self, file_path):
        """Отправляем фото документа user-а"""
        document_file = UserDataFunc.get_document_file(file_path)
        UserApiFuncPositive.document(document_file, headers=self.credentials.auth_header)
        self._update_data_from_server()

    def add_selfie_photo(self, file_path):
        """Отправляем фото сэлфи user-а"""
        selfie_file = UserDataFunc.get_face_file(file_path)
        UserApiFuncPositive.face(selfie_file, headers=self.credentials.auth_header)
        self._update_data_from_server()

    def delete(self):
        """Удаляем пользователя"""
        # сначала удаляем credit_card
        if self.credit_card:
            self.credit_card.delete()
        # затем удаляем user-а
        UserDBFunc.delete_by_id(self.db_client, self.data.id)

    def add_credit_card(self, limit: int = 10):
        """Добавляем новую credit_card"""
        self.credit_card = CreditCard(self.db_client, limit=limit, user_id=self.data.id,
                                      user_auth_header=self.credentials.auth_header)
        self.credit_card.new()
        self._update_data_from_server()

    def compare_data_with_dict(self, user_body, err_msg):
        """Сравниваем self.data с user.body"""
        for key, value in user_body.items():
            assert getattr(self.data, key) == value, err_msg

    def _update_data_from_server(self):
        """Обновляем данные пользователя (получаем данные с server-а)"""
        actual_data = UserApiFuncPositive.get(headers=self.credentials.auth_header)
        self.data.update(actual_data)

    def _get_credential_body(self):
        return {
            "email": self.credentials.email,
            "password": self.credentials.password
        }

    def _get_credential_form(self):
        return {
            "username": self.credentials.email,
            "password": self.credentials.password
        }


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

    # данные для регистрации
    email = "test2@mail.ru"
    password = "password"
    # создаем пользователя
    user2 = User(db_client, email, password)
    # регистрируем пользователя
    user2.register()
    # авторизируем пользователя
    user2.auth()
    # выводим данные текущего пользователя
    print(f"ДО обновления:\n {user2.data}")
    # данные для обновления информации о пользователе
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    user2.update(user_body)
    # выводим данные обновленного пользователя
    print(f"ПОСЛЕ обновления:\n {user2.data}")
    # добавляем документ
    user2.add_document_photo("rus_passport.jpg")
    # добавляем сэлфи
    user2.add_selfie_photo("jolie.jpg")
    # выводим данные обновленного пользователя
    print(f"ПОСЛЕ добавления документа и сэлфи:\n {user2.data}")
    # добавляем новую credit_card
    user2.add_credit_card()
    print(f"кредитная карта:\n {user2.credit_card.data}")
    # пробуем увеличить лимит
    user2.credit_card.increase_limit(3000000)
    print(f"кредитная карта после увеличения лимита:\n {user2.credit_card.data}")
    # закрываем credit_card
    user2.credit_card.close()
    print(f"кредитная карта после закрытия:\n {user2.credit_card.data}")
    # удаляем созданного пользователя
    user2.delete()

    db_client.close_connection()
