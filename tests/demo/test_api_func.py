"""
    Пример написания тестов используя api_func
"""
from http import HTTPStatus

import pytest

from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.data_func import UserDataFunc


@pytest.mark.skip
@pytest.mark.positive
def test_simple_scenario():
    """Простой сценарный тест для user"""
    # данные для регистрации
    credential_body = {
        "email": "test11@mail.ru",
        "password": "password"
    }
    # регистрируем пользователя
    response = UserApiFunc.register(credential_body)
    assert response.status_code == HTTPStatus.OK, "Wrong status code"
    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации по ПРОСТОМУ
    # auth_headers = UserDataFunc.get_auth_header(user_form)
    # получаем header-ы авторизации по СЛОЖНОМУ
    response = UserApiFunc.auth(user_form)
    assert response.status_code == HTTPStatus.OK, "Wrong status code"
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    # выводим данные текущего пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    # TODO проверить status_code
    print(f"ДО обновления:\n {get_response.text}")
    # данные для обновления информации о пользователе
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    update_response = UserApiFunc.update(user_body=user_body, headers=auth_headers)
    # TODO проверить status_code
    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    # TODO проверить status_code
    print(f"ПОСЛЕ обновления:\n {get_response.text}")
    # TODO проверить что get_response.json() соответствует user_body
    # добавляем документ по ПРОСТОМУ
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    # TODO рассказать как будет по сложному
    UserApiFunc.document(document_file, headers=auth_headers)
    # TODO проверить status_code
    # TODO проверить что у пользователя обновился статус по document
    # добавляем сэлфи по ПРОСТОМУ
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    # TODO рассказать как будет по сложному
    UserApiFunc.face(face_file, headers=auth_headers)
    # TODO проверить status_code
    # TODO проверить что у пользователя обновился статус по face
    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"ПОСЛЕ добавления документа и сэлфи:\n {get_response.text}")

    # TODO добавить взаимодействие с credit_card
