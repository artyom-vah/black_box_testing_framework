"""
Основной: Сценарий 2. Клиент банка решил открыть новую кредитную карту в сервисе CreditCard

Альтернативный: Сценарий 8а. Токен авторизации устарел при получении запроса PATCH /user
Альтернативный: Сценарий 8b. Ошибка при обновлении данных пользователя запросом PATCH /user
Альтернативный: Сценарий 10a. Токен авторизации устарел при получении запроса POST /user/document
Альтернативный: Сценарий 11b. Фотография документа не прошла валидацию в Фотосервисе
Альтернативный: Сценарий 14a. Токен авторизации устарел при получении запроса POST /user/face
Альтернативный: Сценарий 15b. Фотография сэлфи не прошла валидацию в Фотосервисе
Альтернативный: Сценарий 19a. Токен авторизации устарел при получении запроса POST /credit_card/new
Альтернативный: Сценарий 20а. У пользователя уже есть открытая КК в БД.
"""

from http import HTTPStatus

import pytest

from src.consts import INVALID_TOKEN
from src.entity.api_entity.credit_card.api_func import CreditCardApiFunc
from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from src.entity.api_entity.user.data_func import UserDataFunc
from tests.conftest import faker_ru


@pytest.mark.scenario
@pytest.mark.positive
@pytest.mark.parametrize('simple_user', [("art4.vakhrushem@mail.ru", "password")], indirect=True)
def test_customer_opens_new_credit_card(simple_user):
    """ Сценарий 2. Клиент банка решил открыть новую кредитную карту в сервисе CreditCard """

    # данные для обновления информации о пользователе
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # проверка - обновляем информацию о пользователе, код 204
    simple_user.update(user_body)

    # проверка - прикрепление фото-документа, код 200
    simple_user.add_document_photo("rus_passport.jpg")

    # проверка - добавление сэлфи, код 200
    simple_user.add_selfie_photo("jolie.jpg")

    # проверка - добавляем новую credit_card, код 200
    simple_user.add_credit_card()

    # проверка информации по открытой КК, код 200
    assert simple_user.credit_card.data.limit, "Wrong status credit_card limit"
    assert simple_user.credit_card.data.balance, "Wrong status credit_card balance"
    assert simple_user.credit_card.data.active, "Wrong status credit_card active"
    assert simple_user.credit_card.data.exp_date, "Wrong status credit_card exp_date"

    # удаляем созданного пользователя
    simple_user.delete()


@pytest.mark.scenario
def test_token_outdated_receiving_pach_user(simple_random_user):
    """ Альтернативный: Сценарий 8а. Токен авторизации устарел при получении запроса PATCH /user """

    # данные для авторизации
    user_form = {
        "username": simple_random_user["email"],
        "password": simple_random_user["password"]
    }

    # выводим данные текущего пользователя
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }

    # обновляем информацию о пользователе
    response = UserApiFunc.update(user_body=user_body, headers=INVALID_TOKEN)

    # проверка на невалидный токен, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, (f"Expected status_code {HTTPStatus.FORBIDDEN},"
                                                          f" but received status_code {response.status_code}")

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    token = UserDataFunc.get_auth_token(user_form)

    # проверка access token и token type получены
    assert "Authorization" in auth_headers, "Authorization header is missing"
    assert auth_headers["Authorization"] == f"Bearer {token}", "Authorization header does not match the expected token"

    # обновляем данные пользователя
    update_response = UserApiFunc.update(user_body=user_body, headers=auth_headers)

    # проверка на валидный токен, код 204
    assert update_response.status_code == HTTPStatus.NO_CONTENT, (f"Expected status_code {HTTPStatus.NO_CONTENT},"
                                                                  f" but received status_code {response.status_code}")


# TODO подумать как сделать этот тест чтобы возварщал 404
# @pytest.mark.scenario
# def test_error_updating_user_data_wit_pach_user():
#     """  Альтернативный: Сценарий 8b. Ошибка при обновлении данных пользователя запросом PATCH /user """
#
#     # выводим данные текущего пользователя
#     user_body = {
#         "full_name": "Иванов Иван Иванович",
#         "income": 40000,
#         "another_loans": False,
#         "birth_date": "1990-01-01",
#         "sex": "male",
#     }
#
#
#     # обновляем данные пользователя
#     update_response = UserApiFunc.update(user_body={}, headers='headers')
#
#     # проверка на валидный токен, код 204
#     # assert update_response.status_code == HTTPStatus.NO_CONTENT, f"Wrong status code {UserApiFunc.__name__}"
#     print(update_response.status_code)

def test_expired_auth_token_post_user_document(simple_random_user):
    """ Сценарий 10a. Токен авторизации устарел при получении запроса POST /user/document """

    # данные для авторизации
    user_form = {
        "username": simple_random_user["email"],
        "password": simple_random_user["password"]
    }

    # добавляем документ
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    response = UserApiFunc.document(document_file, headers=INVALID_TOKEN)

    # проверка регистрации, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, (f"Expected status_code {HTTPStatus.FORBIDDEN},"
                                                          f" but received status_code {response.status_code}")

    # получаем токен авторизации
    token = UserDataFunc.get_auth_token(user_form)

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # проверка access token и token type получены
    assert "Authorization" in auth_headers, "Authorization header is missing"
    assert auth_headers["Authorization"] == f"Bearer {token}", "Authorization header does not match the expected token"

    # добавляем документ
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    response = UserApiFunc.document(document_file, headers=auth_headers)

    # проверка - прикрепление фото-документа, код 200
    assert response.status_code == HTTPStatus.OK, (f"Expected status_code {HTTPStatus.OK},"
                                                   f" but received status_code {response.status_code}")


@pytest.mark.negative
@pytest.mark.user
@pytest.mark.parametrize("document_name, status_code", [
    pytest.param("demo.txt", HTTPStatus.BAD_REQUEST, id='txt file'),
])
def test_add_document_with_bad_format(simple_random_auth_user, document_name, status_code):
    """
    Альтернативный: Сценарий 11b. Фотография документа не прошла валидацию в Фотосервисе
    Альтернативный: Сценарий 15b. Фотография сэлфи не прошла валидацию в Фотосервисе
    """

    # получаем header-ы авторизации для document_file
    auth_header = simple_random_auth_user["auth_header"]
    document_file = UserDataFunc.get_document_file(document_name)

    # document запрос
    response = UserApiFunc.document(document_file, headers=auth_header)

    # провекрка, прикрепление невалидного фотографии-документа, код 400
    assert response.status_code == status_code, f"Expected {status_code}, but received {response.status_code}"
    user_body = UserApiFuncPositive.get(headers=auth_header)
    assert not user_body["status_document"], "Wrong status_document after add document"

    # получаем header-ы авторизации для face_file
    auth_header = simple_random_auth_user["auth_header"]
    face_file = UserDataFunc.get_face_file(document_name)

    # document запрос
    response = UserApiFunc.face(face_file, headers=auth_header)

    # провекрка, прикрепление невалидного фото-лица, код 400
    assert response.status_code == status_code, "Wrong status code"
    user_body = UserApiFuncPositive.get(headers=auth_header)
    assert not user_body["status_document"], "Wrong status_document after add document"


def test_expired_auth_token_post_user_face(simple_random_user):
    """Альтернативный: Сценарий 14a. Токен авторизации устарел при получении запроса POST /user/face"""

    # данные для авторизации
    user_form = {
        "username": simple_random_user["email"],
        "password": simple_random_user["password"]
    }

    # добавляем документ
    document_file = UserDataFunc.get_face_file("jolie.jpg")
    response = UserApiFunc.document(document_file, headers=INVALID_TOKEN)

    # проверка регистрации, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, f"Wrong status code {UserApiFunc.__name__}"

    # получаем токен авторизации
    token = UserDataFunc.get_auth_token(user_form)

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)

    # проверка access token и token type получены
    assert "Authorization" in auth_headers, "Authorization header is missing"
    assert auth_headers["Authorization"] == f"Bearer {token}", "Authorization header does not match the expected token"

    # добавляем документ
    document_file = UserDataFunc.get_face_file("jolie.jpg")
    response = UserApiFunc.document(document_file, headers=auth_headers)

    # проверка - прикрепление фото-документа, код 200
    assert response.status_code == HTTPStatus.OK, f"Wrong status code {UserApiFunc.__name__}"


def test_token_expired_when_receiving_post_credit_card_new():
    """ Альтернативный: Сценарий 19a. Токен авторизации устарел при получении запроса POST /credit_card/new """

    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }

    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    limit_params = {"limit": 1000000}
    response = CreditCardApiFunc.new(limit_params, headers=INVALID_TOKEN)

    # проверка открытия новой КК с устаревшим токеном, код 403
    assert response.status_code == HTTPStatus.FORBIDDEN, f"Wrong status code {UserApiFunc.__name__}"

    # получаем header-ы авторизации
    token = UserDataFunc.get_auth_token(user_form)
    auth_headers = UserDataFunc.get_auth_header(user_form)
    assert "Authorization" in auth_headers, "Authorization header is missing"
    assert auth_headers["Authorization"] == f"Bearer {token}", "Authorization header does not match the expected token"

    # открываем кредитную карту
    response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка открытия новой карты, код 200
    assert response.status_code == HTTPStatus.OK, f"Wrong status code {UserApiFunc.__name__}"


def test_user_already_open_credit_card():
    """ Альтернативный: Сценарий 20а. У пользователя уже есть открытая КК в БД """

    # данные для авторизации
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

    # добавляем лимит у новой карты
    limit_params = {"limit": 1000000}

    # заводим новую кредитную карту
    CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # пытаемся завести 2 кредитную карту
    response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка - у уже пользователя есть КК, код 400
    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Wrong status code{response.status_code}"
