"""
    Функции для работы с данными из body-ответов user-а
"""
from dataclasses import dataclass

import dpath
from strenum import StrEnum

from src.consts import get_document_file_path, get_face_file_path
from src.entity.api_entity.user.api_func_positive import UserApiFuncPositive


class _UserBodyPath(StrEnum):
    """Константы с путями в body для user"""
    token = "access_token"


class UserDataFunc:
    @staticmethod
    def get_auth_token(credential_form: dict):
        """Получаем token авторизации для user-а"""
        body = UserApiFuncPositive.auth(credential_form)
        # получаем token
        token = dpath.get(body, _UserBodyPath.token, separator='.')
        # token = body["access_token"]
        return token

    @staticmethod
    def get_auth_header(credential_form: dict):
        """Получаем header-ы с token-ом авторизации для user-а"""
        token = UserDataFunc.get_auth_token(credential_form)
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def get_document_file(document_name):
        """Получаем body c документом для отправки в сервис"""
        document_path = get_document_file_path(document_name)
        return {"file": open(document_path, 'rb')}

    @staticmethod
    def get_document_files(document_name_list):
        """Получаем body c документом для отправки в сервис"""
        file_body = []
        for document_name in document_name_list:
            document_path = get_document_file_path(document_name)
            file_body.append(("file", (open(document_path, 'rb'))))
        return file_body

    @staticmethod
    def get_face_file(face_name):
        """Получаем body c фото-селфи для отправки в сервис"""
        face_path = get_face_file_path(face_name)
        return {"file": open(face_path, 'rb')}


if __name__ == "__main__":
    # auth_form = {
    #     "username": "test1@mail.ru",
    #     "password": "password"
    # }
    # header = UserDataFunc.get_auth_header(auth_form)
    # print(header)
    # UserDataFunc.get_document_file("rus_passport.jpg")
    file_body = UserDataFunc.get_document_files(["demo.txt", "rus_passport.jpg"])
    pass
