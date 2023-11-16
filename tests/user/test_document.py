"""Тесты для проверки api-запроса document"""
from http import HTTPStatus

import pytest

from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive
from src.entity.api_entity.user.data_func import UserDataFunc


@pytest.mark.positive
@pytest.mark.user
def test_add_document_successful(simple_random_auth_user):
    """Успешное добавление фото пасспорта пользователя"""
    auth_header = simple_random_auth_user["auth_header"]
    document_body = UserDataFunc.get_document_file("rus_passport.jpg")
    # document запрос
    UserApiFuncPositive.document(document_body, headers=auth_header)
    user_body = UserApiFuncPositive.get(headers=auth_header)
    assert user_body["status_document"], "Wrong status_document after add document"


@pytest.mark.negative
@pytest.mark.user
@pytest.mark.parametrize("document_name, status_code", [
    pytest.param("demo.txt", HTTPStatus.BAD_REQUEST, id='txt file'),
])
def test_add_document_with_bad_format(simple_random_auth_user, document_name, status_code):
    """Попытка добавить фото документа НЕ правильного формата"""
    auth_header = simple_random_auth_user["auth_header"]
    document_body = UserDataFunc.get_document_file(document_name)
    # document запрос
    response = UserApiFunc.document(document_body, headers=auth_header)
    assert response.status_code == status_code, "Wrong status code"
    user_body = UserApiFuncPositive.get(headers=auth_header)
    assert not user_body["status_document"], "Wrong status_document after add document"


@pytest.mark.negative
@pytest.mark.user
def test_add_multiple_documents(simple_random_auth_user):
    """Успешное добавление фото пасспорта пользователя"""
    auth_header = simple_random_auth_user["auth_header"]
    document_body = UserDataFunc.get_document_files(["rus_passport.jpg", "rus_passport2.jpg"])
    # document запрос
    response = UserApiFunc.document(document_body, headers=auth_header)
    user_body = UserApiFuncPositive.get(headers=auth_header)
    assert user_body["status_document"], "Wrong status_document after add document"
