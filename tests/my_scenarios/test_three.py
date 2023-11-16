"""
Сценарий 3. Клиент банка с открытой кредитной картой хочет увеличить лимит по карте

Альтернативный: Сценарий 2а. Токен авторизации устарел при получении запроса GET /credit_card
Альтернативный: Сценарий 9a. Токен авторизации устарел при получении запроса GET /user
Альтернативный: Сценарий 11а. У пользователя нет проверенного фото ДУЛ
Альтернативный: Сценарий 11b. У пользователя нет проверенного фото сэлфи
Альтернативный: Сценарий 11с. У пользователя нет проверенных фото ДУЛ и сэлфи Сценарий
Альтернативный: Сценарий 13a. Токен авторизации устарел при получении запроса POST /credit_card/increase_limit.
Альтернативный: Сценарий 15а. Текущий лимит по карте превышает запрошенный лимит
Альтернативный: Сценарий 17а. Текущий лимит по карте превышает рассчитанный увеличенный лимит

"""
from http import HTTPStatus

import pytest

from src.consts import INVALID_TOKEN, STANDART_LIMIT
from src.entity.api_entity.credit_card.api_func import CreditCardApiFunc
from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.data_func import UserDataFunc
from tests.conftest import faker_ru


@pytest.mark.scenario
@pytest.mark.positive
@pytest.mark.parametrize('user_test_three', [("art5.vakhrushem@mail.ru", "password")], indirect=True)
def test_bank_customer_open_card_increase_limit(user_test_three):
    """ Сценарий 3. Клиент банка с открытой кредитной картой хочет увеличить лимит по карте """

    # проверка информации по открытой КК, код 200
    assert user_test_three.credit_card.data, "Wrong status credit_card"

    # проверка информации каждого пункта по открытой КК
    assert user_test_three.credit_card.data.limit, "Wrong status credit_card limit"
    assert user_test_three.credit_card.data.balance, "Wrong status credit_card balance"
    assert user_test_three.credit_card.data.active, "Wrong status credit_card active"
    assert user_test_three.credit_card.data.exp_date, "Wrong status credit_card exp_date"

    # проверяем лимит credit_card равен лимиту установленному по-умолчанию (2_000_000)
    assert user_test_three.credit_card.data.limit == STANDART_LIMIT

    # проверка запроса на увеличение лимита, код 200
    user_test_three.credit_card.increase_limit(3_000_000)

    # проверка информация о пользователе, код 200
    assert user_test_three.data, "Wrong status user"

    # проверяем что лимит увеличился до 3_000_000
    assert user_test_three.credit_card.data.limit == 3_000_000

    # проверка информации по открытой КК
    assert user_test_three.credit_card.data.limit, "Wrong status credit_card"

    # проверка информация о пользователе, код 200
    assert user_test_three.data.full_name, "Wrong status full_name"
    assert user_test_three.data.income, "Wrong status income"
    assert user_test_three.data.birth_date, "Wrong status birth_date"
    assert user_test_three.data.sex, "Wrong status sex"
    assert user_test_three.data.email, "Wrong status email"
    assert user_test_three.data.status_document, "Wrong status_document"
    assert user_test_three.data.status_face, "Wrong status_face"


def test_authorization_token_outdated_with_get_credit_card():
    """ Альтернативный: Сценарий 2а. Токен авторизации устарел при получении запроса GET /credit_card """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # заводим новую кредитную карту
    limit_params = {"limit": 1000000}
    CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # получаем информацию по карте с невалидным токеном
    invalid_token = CreditCardApiFunc.get(headers=INVALID_TOKEN)

    # проверка на невалидный токен, код 403
    assert invalid_token.status_code == HTTPStatus.FORBIDDEN, f"Wrong status code {invalid_token.CreditCardApiFunc.__name__}"

    # получаем информацию по карте
    response = CreditCardApiFunc.get(headers=auth_headers)

    expected_keys = ['limit', 'balance', 'active', 'exp_date']

    # Проверить, что все ключи присутствуют в словаре
    for key in expected_keys:
        assert key in response.text, f"Key {key} not found in the JSON data"

    expected_keys_count = 4

    assert len(response.json()) == expected_keys_count, "Expected number of keys in JSON-response does not match."


def test_authorization_token_outdated_with_get_user():
    """ Альтернативный: Сценарий 9a. Токен авторизации устарел при получении запроса GET /user """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }

    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # получаем информацию по пользователю с невалидным токеном
    response = UserApiFunc.get(headers=INVALID_TOKEN)

    # проверка на невалидный токен, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, f"Wrong status code {UserApiFunc.__name__}"

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    auth_headers = UserDataFunc.get_auth_header(user_form)
    get_response = UserApiFunc.get(headers=auth_headers)

    # проверка регистрации, код 200
    assert get_response.status_code == HTTPStatus.OK, f"Wrong status code {UserApiFunc.__name__}"

    response_data = get_response.json()

    # проверка формата данных
    assert isinstance(response_data, dict), "Response data is not in the expected format (dict)"
    print(response_data)

    # проверка количества ключей в ответе
    expected_keys_count = 8
    assert len(
        response_data) == expected_keys_count, f"Expected {expected_keys_count} keys in the response, but found {len(response_data)}"

    # проверка ожидаемых ключей в ответе
    expected_keys = ["full_name", "income", "another_loans", "birth_date", "sex", "email", "status_document",
                     "status_face"]

    # Проверить, что все ключи присутствуют в словаре
    for key in expected_keys:
        assert key in response_data, f"Key '{key}' is missing in the response data"


@pytest.mark.scenario
@pytest.mark.positive
@pytest.mark.parametrize('simple_user', [("art.vakhrushem@mail.ru", "password")], indirect=True)
def test_user_does_not_verified_photo(simple_user):
    """
    Альтернативный: Сценарий 11а. У пользователя нет проверенного фото ДУЛ
    Альтернативный: Сценарий 11b. У пользователя нет проверенного фото сэлфи
    Альтернативный: Сценарий 11с. У пользователя нет проверенных фото ДУЛ и сэлфи Сценарий
    """

    # данные для обновления информации о пользователе
    update_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    #  обновляем информацию о пользователе
    simple_user.update(update_body)

    # проверка добавления документа, код 200
    simple_user.add_document_photo("rus_passport.jpg")
    assert simple_user.data.status_document, "Wrong status_document"

    # проверка добавления сэлфи, код 200
    simple_user.add_selfie_photo("jolie.jpg")
    assert simple_user.data.status_face, "Wrong status_status_face"


@pytest.mark.scenario
def test_authorization_token_outdated_with_post_credit_card_increase_limit():
    """Альтернативный: Сценарий 13a. Токен авторизации устарел при получении запроса POST/credit_card/increase_limit """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # заводим новую кредитную карту
    limit_params = {"limit": 1000000}
    response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # добавляем документ - чтобы корректно увеличить лимит
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # увеличиваем лимит по карте
    limit_params = {"limit": 3000000}

    # проверка на невалидный токен, код 403
    response = CreditCardApiFunc.increase_limit(limit_params, headers=INVALID_TOKEN)
    assert response.status_code == HTTPStatus.FORBIDDEN, f"Wrong status code {CreditCardApiFunc.__name__}"

    # получаем header-ы авторизации
    token = UserDataFunc.get_auth_token(user_form)
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # проверка повторной авторизации, access token и token type получены
    assert "Authorization" in auth_headers, "Authorization header is missing"
    assert auth_headers["Authorization"] == f"Bearer {token}", "Authorization header does not match the expected token"

    # проверка на увеличение лимита по КК с валидным токеном, код 200
    response = CreditCardApiFunc.increase_limit(limit_params, headers=auth_headers)
    assert response.status_code == HTTPStatus.OK, f"Wrong status code {CreditCardApiFunc.__name__}"


@pytest.mark.scenario
def test_current_limit_exceeds_requested_limit():
    """ Альтернативный: Сценарий 15а. Текущий лимит по карте превышает запрошенный лимит """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации и заводим новую кредитную карту
    limit_params = {"limit": 1000000}
    CreditCardApiFunc.new(limit_params, headers=UserDataFunc.get_auth_header(user_form))

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # увеличиваем лимит по карте
    limit_params = {"limit": 10000}

    # проверка - запрашиваемый лимит меньше текущего, код 400
    response = CreditCardApiFunc.increase_limit(limit_params, headers=auth_headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Wrong status code {CreditCardApiFunc.__name__}"


@pytest.mark.scenario
def test_current_limit_card_exceeds_calculated_increased_limit():
    """ Альтернативный: Сценарий 17а. Текущий лимит по карте превышает рассчитанный увеличенный лимит """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    # регистрируем пользователя
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации и заводим новую кредитную карту
    limit_params = {"limit": 1000000}
    CreditCardApiFunc.new(limit_params, headers=UserDataFunc.get_auth_header(user_form))

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # увеличиваем лимит по карте
    limit_params = {"limit": 3000000}

    # проверка - "Увеличение лимита недоступно с текущими параметрами, код 400
    response = CreditCardApiFunc.increase_limit(limit_params, headers=auth_headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Wrong status code {CreditCardApiFunc.__name__}"
