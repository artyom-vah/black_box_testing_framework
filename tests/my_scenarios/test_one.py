"""
Сценарии тестирования:

Сценарий 1. Пользователь впервые регистрируется и проходит авторизацию в сервисе CreditCard.

Альтернативный: Сценарий 5a. Пользователь уже зарегистрирован в БД БКК
Альтернативный: Сценарий 5b, 7a. Введенный email не соответствует формату
Альтернативный: Сценарий 5с, 7b. Введенный password не соответствует формату

"""
from http import HTTPStatus

import pytest

from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.high_level.user import User
from tests.conftest import faker_ru


@pytest.mark.scenario
@pytest.mark.positive
def test_user_registers_first_time_and_authorized_in_credit_card(db_client):
    """ Сценарий 1. Пользователь впервые регистрируется и проходит авторизацию в сервисе CreditCard """

    # данные для регистрации
    email = "art3.vakhrushem@mail.ru"
    password = "password"

    # создаем пользователя
    user = User(db_client, email, password)

    # доп. проверка статус email в статусе None
    assert user.data.email is None, f"email has status not None"

    # проверка пользователь зарегистрировался, код 200
    user.register()

    # проверка пользователь авторизовался, код 200
    user.auth()

    # доп. проверка статуса email изменился
    assert user.data.email, f"email status has changed from None to {email}"

    # удаляем созданного пользователя из бд
    user.delete()
    db_client.close_connection()


@pytest.mark.negative
@pytest.mark.user
def test_user_with_this_email_address_already_exists():
    """ Альтернативный: Сценарий 5a. Пользователь уже зарегистрирован в БД БКК (соответствует требованиям 5а) """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }

    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # повторная регистрируем зарегистрированного пользователя
    response = UserApiFunc.register(credential_body)

    # проверка пользователь уже зарегистрирован, код 400
    assert response.status_code == HTTPStatus.BAD_REQUEST, (f"Expected status_code {HTTPStatus.BAD_REQUEST},"
                                                            f" but received status_code {response.status_code}")


@pytest.mark.negative
@pytest.mark.user
@pytest.mark.parametrize("email, password", [
    pytest.param(1, 'password', id='email is INT'),
    pytest.param("abcd", 'password', id='email is STR'),
    pytest.param("email1@mail.ru", 1, id='password is int'),
    pytest.param("", '', id='email and password are EMPTY'),
    pytest.param(None, 'password', id='email is None'),
    pytest.param("email@mail.ru", None, id='password is None'),

])
def test_email_password_with_bad_data_format(email, password):
    """
    Альтернативный: Сценарий 5b, 7a. Введенный email не соответствует формату
    Альтернативный: Сценарий 5с, 7b. Введенный password не соответствует формату
    """

    # данные для регистрации
    credential_form = {
        "email": email,
        "password": password
    }

    # регистрируем пользователя
    response = UserApiFunc.auth(credential_form)

    # проверка формата email и password, код 422
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, f"Wrong status code {response.status_code}"
