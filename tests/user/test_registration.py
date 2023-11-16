"""Тесты для проверки api для registration"""

from http import HTTPStatus

import pytest

from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from src.entity.db_entity.user.db_func import UserDBFunc
from tests.config import faker_ru


@pytest.mark.positive
@pytest.mark.user
def test_registration_success(db_client):
    """Успешная регистрация"""
    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFuncPositive.register(credential_body)
    # TODO подумать что еще можно проверить кроме статус кода
    # удаляем созданного пользователя
    user_id = UserDBFunc.get_id(db_client, credential_body["email"])
    UserDBFunc.delete_by_id(db_client, user_id)


# TODO создать тест который бы проверял граничные значения по длине email и password

@pytest.mark.negative
@pytest.mark.user
def test_already_registered_user(simple_random_user):
    """Попытка регистрации уже существующего пользователя"""
    response = UserApiFunc.register(simple_random_user)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.negative
@pytest.mark.user
@pytest.mark.parametrize("email, password", [
    pytest.param(1, 'password', id='email is INT'),
    pytest.param([1, 2, 3], 'password', id='email is LIST'),
    pytest.param("email1@mail.ru", 1, id='password is int'),
    # TODO дописать кейсов
])
def test_registraion_with_bad_data_format(email, password):
    """Попытка регистрации с данными не в том формате"""
    # данные для регистрации
    credential_body = {
        "email": email,
        "password": password
    }
    # регистрируем пользователя
    response = UserApiFunc.register(credential_body)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
