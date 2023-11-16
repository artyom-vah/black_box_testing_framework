"""Тесты для проверки api-запроса auth"""

from http import HTTPStatus

import pytest

from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from tests.conftest import faker_ru


@pytest.mark.positive
@pytest.mark.user
def test_auth_user_successful(simple_random_user):
    """Успешная авторизация пользователя"""
    # получаем auth_header
    credential_form = {
        "username": simple_random_user["email"],
        "password": simple_random_user["password"]
    }
    body = UserApiFuncPositive.auth(credential_form)
    assert "access_token" in body.keys(), "Key access_token not in AUTH user_body"
    assert isinstance(body["access_token"], str), "access_token is not STR"


@pytest.mark.negative
@pytest.mark.user
@pytest.mark.parametrize("email, password", [
    pytest.param(1, 'password', id='email is INT'),
    pytest.param([1, 2, 3], 'password', id='email is LIST'),
    pytest.param("email1@mail.ru", 1, id='password is int'),
    # TODO дописать кейсов
])
def test_auth_with_bad_data_format(email, password):
    """Попытка авторизации с данными не в том формате"""
    # данные для регистрации
    credential_form = {
        "email": email,
        "password": password
    }
    # регистрируем пользователя
    response = UserApiFunc.auth(credential_form)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.negative
@pytest.mark.user
def test_auth_with_not_exist_email():
    """Попытка авторизации НЕ существующего пользователя"""
    # данные для регистрации
    credential_form = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    response = UserApiFunc.auth(credential_form)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.negative
@pytest.mark.user
def test_auth_user_with_incorrect_password(simple_random_user):
    """Попытка авторизация существующего пользователя с некорректным паролем"""
    # получаем auth_header
    credential_form = {
        "username": simple_random_user["email"],
        "password": faker_ru.password()
    }
    response = UserApiFunc.auth(credential_form)
    assert response.status_code == HTTPStatus.BAD_REQUEST
