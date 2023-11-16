"""
    Общие фикстуры для тестов
"""
import os

import pytest

from src.clients.db import DBClient
from src.consts import EnvName
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from src.entity.api_entity.user.data_func import UserDataFunc
from src.entity.db_entity.user.db_func import UserDBFunc
from src.entity.high_level.user import User
from tests.config import faker_ru


@pytest.fixture(scope="session")
def db_client():
    """Получаем клиента к БД"""
    db_credential = (
        os.getenv(EnvName.DB_NAME),
        os.getenv(EnvName.DB_USER),
        os.getenv(EnvName.DB_PASSWORD),
        os.getenv(EnvName.DB_HOST),
        os.getenv(EnvName.DB_PORT)
    )
    db_client = DBClient()
    db_client.create_connection(*db_credential)
    yield db_client
    db_client.close_connection()


@pytest.fixture(scope="function")
def simple_random_user(db_client):
    """Регистрируем пустого user со случайным email и password"""
    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFuncPositive.register(credential_body)
    yield credential_body
    # удаляем созданного пользователя
    user_id = UserDBFunc.get_id(db_client, credential_body["email"])
    UserDBFunc.delete_by_id(db_client, user_id)


@pytest.fixture(scope="function")
def simple_random_auth_user(simple_random_user):
    """Регистрируем пустого user со случайным email и password + получаем auth_header"""
    # получаем auth_header
    credential_form = {
        "username": simple_random_user["email"],
        "password": simple_random_user["password"]
    }
    auth_header = UserDataFunc.get_auth_header(credential_form)
    return {"credential": simple_random_user,
            "auth_header": auth_header}


# ВСЁ ЧТО НИЖЕ ПОКА НЕ СМОТРЕТЬ
@pytest.fixture(scope="session")
def user1(db_client):
    """Регистрируем User1 - для тестов где нужен просто зарегистрированный пользователь"""
    email = os.getenv(EnvName.USER1_EMAIL)
    password = os.getenv(EnvName.USER1_PASSWORD)
    # создаем пользователя
    user1 = User(db_client, email, password)
    # регистрируем пользователя
    user1.register()
    # авторизируем пользователя
    user1.auth()
    yield user1
    user1.delete()


@pytest.fixture(scope="function")
def simple_user(db_client, request) -> User:
    """Регистрируем пустого user"""
    # для каждого теста использующего эту фикстуру будет создан СВОЙ пользователь с заданными email и password
    # после завершения теста - этот пользователь будет удален
    email, password = request.param
    # создаем пользователя
    user = User(db_client, email, password)
    # регистрируем пользователя
    user.register()
    # авторизируем пользователя
    user.auth()
    yield user
    user.delete()


@pytest.fixture(scope="function")
def user_test_three(db_client, request) -> User:
    """ Юзер для тестов 3-го сценария """
    email, password = request.param
    # создаем пользователя
    user = User(db_client, email, password)
    # регистрируем пользователя
    user.register()
    # авторизируем пользователя
    user.auth()
    # данные для обновления информации о пользователе
    update_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    user.update(update_body)
    # проверяем что все обновилось корректно (проверка что update_body соответствует данным на сервере)
    user.compare_data_with_dict(update_body, "Error on UPDATE User")
    # добавляем документ
    user.add_document_photo("rus_passport.jpg")
    # добавляем сэлфи
    user.add_selfie_photo("jolie.jpg")
    # выводим данные обновленного пользователя
    # добавляем новую credit_card
    user.add_credit_card()
    yield user
    user.delete()


@pytest.fixture(scope="function")
def user_test_four(db_client, request) -> User:
    """ Юзер для тестов 4-го сценария """
    email, password = request.param
    # создаем пользователя
    user = User(db_client, email, password)
    # регистрируем пользователя
    user.register()
    # авторизируем пользователя
    user.auth()
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    user.update(user_body)
    # добавляем документ
    user.add_document_photo("rus_passport.jpg")
    # добавляем сэлфи
    user.add_selfie_photo("jolie.jpg")
    # добавляем новую credit_card
    user.add_credit_card()
    yield user
    user.delete()
