"""
Сценарии тестирования:
Основной: Сценарий 4. Клиент банка с открытой кредитной картой хочет закрыть карту

Альтернативный: Сценарий 2a. Токен авторизации устарел при получении запроса GET /user
Альтернативный: Сценарий 7a. Токен авторизации устарел при получении запроса POST /credit_card/close

Альтернативный: Сценарий 2a. Токен авторизации устарел при получении запроса GET /user (по сложному)
Альтернативный: Сценарий 7a. Токен авторизации устарел при получении запроса POST /credit_card/close (по сложному)
"""

from http import HTTPStatus

import pytest

from src.consts import INVALID_TOKEN
from src.entity.api_entity.credit_card.api_func import CreditCardApiFunc
from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.data_func import UserDataFunc
from tests.conftest import faker_ru


@pytest.mark.scenario
@pytest.mark.positive
@pytest.mark.parametrize('user_test_four', [("art6.vakhrushem@mail.ru", "password")], indirect=True)
def test_customer_with_open_credit_card_wants_close_card(user_test_four):
    """ Сценарий 4. Клиент банка с открытой кредитной картой хочет закрыть карту """

    # проверка информации по открытой КК
    assert user_test_four.credit_card.data.limit, "Wrong status credit_card limit"
    assert user_test_four.credit_card.data.balance, "Wrong status credit_card balance"
    assert user_test_four.credit_card.data.active, "Wrong status credit_card active"
    assert user_test_four.credit_card.data.exp_date, "Wrong status credit_card exp_date"

    # проверка закрытия credit_card, код 200
    user_test_four.credit_card.close()

    # проверка статуса КК - не активен
    assert not user_test_four.credit_card.data.active, "Status credit_card is active"


@pytest.mark.scenario
@pytest.mark.parametrize('user_test_four', [("art1.vakhrushem@mail.ru", "password")], indirect=True)
def test_token_is_outdated_on_get_user(user_test_four):
    """ Альтернативный: Сценарий 2a. Токен авторизации устарел при получении запроса GET /user """

    # получаем невалидные headers
    response = UserApiFunc.get(headers=INVALID_TOKEN)

    # проверка пользователь авторизовался с невалидным токеном, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, (f"Expected status_code {HTTPStatus.FORBIDDEN},"
                                                          f" but received status_code {response.status_code}")

    # проверка получения информации о пользователе, код 200
    assert user_test_four.data


@pytest.mark.scenario
@pytest.mark.parametrize('user_test_four', [("art2.vakhrushem@mail.ru", "password")], indirect=True)
def test_token_is_outdated_on_post_credit_card(user_test_four):
    """ Альтернативный: Сценарий 7a. Токен авторизации устарел при получении запроса POST /credit_card/close """

    # получаем невалидные headers
    response = UserApiFunc.get(headers=INVALID_TOKEN)

    # проверка пользователь авторизовался с невалидным токеном, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, (f"Expected status_code {HTTPStatus.FORBIDDEN},"
                                                          f" but received status_code {response.status_code}")

    # проверка закрытия карты, код 200
    user_test_four.credit_card.close()

    # проверка статуса карты - не активный, код 200
    assert not user_test_four.credit_card.data.active


@pytest.mark.positive
def test_token_is_outdated_on_get_user_2():
    """ Альтернативный: Сценарий 2a. Токен авторизации устарел при получении запроса GET /user (по сложному)"""

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # выводим данные текущего пользователя
    response = UserApiFunc.get(headers=INVALID_TOKEN)

    # проверка пользователь авторизовался с невалидным токеном, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, (f"Expected status_code {HTTPStatus.FORBIDDEN},"
                                                          f" but received status_code {response.status_code}")

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # авторизуем пользователя с валидным токеном
    response = UserApiFunc.auth(user_form)

    # проверка пользователь авторизовался с валидным токеном, код 200
    assert response.status_code == HTTPStatus.OK, (f"Expected status_code {HTTPStatus.OK},"
                                                   f" but received status_code {response.status_code}")
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    # получаем информацию о пользователе
    get_response = UserApiFunc.get(headers=auth_headers)

    # проверка
    assert get_response.status_code == HTTPStatus.OK, "Wrong status code"
    response_data = get_response.json()
    # проверка формата данных
    assert isinstance(response_data, dict), "Response data is not in the expected format (dict)"

    # проверка количества ключей в ответе
    expected_keys_count = 8
    assert len(response_data) == expected_keys_count, (f"Expected {expected_keys_count} keys in the response, but found"
                                                       f"{len(response_data)}")
    # проверяем ожидаемые ключи в ответе
    expected_keys = ["full_name", "income", "another_loans", "birth_date", "sex", "email", "status_document",
                     "status_face"]
    for key in expected_keys:
        assert key in response_data, f"Key '{key}' is missing in the response data"


def test_token_is_outdated_on_post_credit_card_2():
    """
    Альтернативный: Сценарий 7a. Токен авторизации устарел при получении запроса POST /credit_card/close (по сложному)
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # данные для авторизации
    credential_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(credential_form)

    # заводим новую кредитную карту
    limit_params = {"limit": 1000000}
    CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # пытаемся закрыть КК с невалидным токеном
    close_cart_response = CreditCardApiFunc.close(headers=INVALID_TOKEN)

    # проверка пользователь авторизовался с невалидным токеном, код 403
    assert close_cart_response.status_code == HTTPStatus.FORBIDDEN, (f"Expected status_code {HTTPStatus.FORBIDDEN},"
                                                                     f" but received status_code"
                                                                     f" {close_cart_response.status_code}")

    # получаем токен авторизации
    token = UserDataFunc.get_auth_token(credential_form)

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(credential_form)

    # проверка access token и token type получены
    assert "Authorization" in auth_headers, "Authorization header is missing"
    assert auth_headers["Authorization"] == f"Bearer {token}", "Authorization header does not match the expected token"

    # закрываем кредитную карту
    response = CreditCardApiFunc.close(headers=auth_headers)
    assert response.status_code == HTTPStatus.OK, (f"Expected status_code {HTTPStatus.OK},"
                                                   f" but received status_code {response.status_code}")
