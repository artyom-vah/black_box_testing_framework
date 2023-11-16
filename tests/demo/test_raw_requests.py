"""
    Пример написания тестов используя голый requests
"""
import os
from http import HTTPStatus

import pytest
import requests

from src.consts import (DATA_FOLDER, DOCUMENT_FOLDER, FACE_FOLDER, ROOT_PATH,
                        TEST_FOLDER)


@pytest.mark.skip
@pytest.mark.positive
def test_simple_scenario():
    """Простой сценарный тест для user"""
    # данные для регистрации
    credential_body = {
        "email": "test12@mail.ru",
        "password": "password"
    }
    # регистрируем пользователя
    response = requests.post(url="http://127.0.0.1:8000/user/register", json=credential_body)
    assert response.status_code == HTTPStatus.OK, "Wrong status code"
    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    response = requests.post(url="http://127.0.0.1:8000/auth/access_token", data=user_form)
    assert response.status_code == HTTPStatus.OK, "Wrong status code"
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    # выводим данные текущего пользователя
    get_response = requests.get(url="http://127.0.0.1:8000/user", headers=auth_headers)
    # TODO проверить status_code
    # данные для обновления информации о пользователе
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    update_response = requests.patch(url="http://127.0.0.1:8000/user", json=user_body, headers=auth_headers)
    # TODO проверить status_code
    # выводим данные обновленного пользователя
    get_response = requests.get(url="http://127.0.0.1:8000/user", headers=auth_headers)
    # TODO проверить status_code
    # TODO проверить что get_response.json() соответствует user_body
    # добавляем документ
    document_name = "rus_passport.jpg"
    document_path = os.path.join(ROOT_PATH, TEST_FOLDER, DATA_FOLDER, DOCUMENT_FOLDER, document_name)
    document_file = {"file": open(document_path, 'rb')}
    requests.post(url="http://127.0.0.1:8000/user/document", files=document_file, headers=auth_headers)
    # TODO проверить status_code
    # TODO проверить что у пользователя обновился статус по document
    # добавляем сэлфи по ПРОСТОМУ
    face_name = "jolie.jpg"
    face_path = os.path.join(ROOT_PATH, TEST_FOLDER, DATA_FOLDER, FACE_FOLDER, face_name)
    face_file = {"file": open(face_path, 'rb')}
    requests.post(url="http://127.0.0.1:8000/user/face", files=face_file, headers=auth_headers)
    # TODO проверить status_code
    # TODO проверить что у пользователя обновился статус по face
    # выводим данные обновленного пользователя
    get_response = requests.get(url="http://127.0.0.1:8000/user", headers=auth_headers)

    # TODO добавить взаимодействие с credit_card
