"""Тесты для проверки api-запроса GET"""

from http import HTTPStatus

import pytest

from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from src.entity.api_entity.user.data_func import UserDataFunc


@pytest.mark.positive
@pytest.mark.user
def test_get_user_successful(simple_random_auth_user):
    """Успешное получение информации о пользователе"""
    auth_header = simple_random_auth_user["auth_header"]
    # GET запрос
    user_body = UserApiFuncPositive.get(headers=auth_header)
    # ключи которые должны быть в теле user_body
    get_body_keys = ['another_loans', 'birth_date', 'email', 'full_name', 'income', 'sex', 'status_document',
                     'status_face']
    # проверяем что все ключи присутствуют
    for key in get_body_keys:
        assert key in user_body.keys(), f"Key {key} not in GET user_body"
        # TODO подумать дома чтобы работало как надо
    # TODO расказать про pydantic


@pytest.mark.parametrize("auth_header, status_code", [
    pytest.param(None, HTTPStatus.UNAUTHORIZED, id='None'),
    pytest.param("", HTTPStatus.UNAUTHORIZED, id='empty str'),
    pytest.param({"Authorization": f"Bearer 123"}, HTTPStatus.FORBIDDEN, id='BAD token'),
    # pytest.param({"Authorization": f"Bearer {NOT_FOUND_TOKEN}"}, HTTPStatus.NOT_FOUND, id='NOT FOUND token')
    # TODO дописать кейсов
])
@pytest.mark.negative
@pytest.mark.user
def test_get_user_with_bad_auth_header(simple_random_user, auth_header, status_code):
    """Успешное получение информации о пользователе"""
    response = UserApiFunc.get(headers=auth_header)
    assert response.status_code == status_code
