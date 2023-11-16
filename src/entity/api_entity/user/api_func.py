"""
    API-функции для работы с сущностью user
"""

from src.clients.api import ApiClient
from src.entity.api_entity.user.api_path import UserFullPath


class UserApiFunc:
    @staticmethod
    def register(credential_body: dict, **kwargs):
        """Регистрируем user-а"""
        return ApiClient.post(url=UserFullPath.register, json=credential_body, **kwargs)

    @staticmethod
    def auth(credential_form: dict, **kwargs):
        """Авторизуем user-а"""
        return ApiClient.post(url=UserFullPath.auth, data=credential_form, **kwargs)

    @staticmethod
    def get(**kwargs):
        """Получаем текущего user-а"""
        return ApiClient.get(url=UserFullPath.get, **kwargs)

    @staticmethod
    def update(user_body: dict, **kwargs):
        """Обновляем текущего user-а"""
        return ApiClient.patch(url=UserFullPath.patch, json=user_body, **kwargs)

    @staticmethod
    def document(files, **kwargs):
        """Отправляем фото документа user-а"""
        return ApiClient.post(url=UserFullPath.document, files=files, **kwargs)

    @staticmethod
    def face(files, **kwargs):
        """Отправляем фото сэлфи user-а"""
        return ApiClient.post(url=UserFullPath.face, files=files, **kwargs)


if __name__ == "__main__":
    from entity.api_entity.user.data_func import UserDataFunc

    # данные для регистрации
    credential_body = {
        "email": "test1@mail.ru",
        "password": "password"
    }
    # # регистрируем пользователя
    # response = UserApiFunc.register(credential_body)
    # assert response.status_code == HTTPStatus.OK, f"Wrong status code {UserApiFunc.__name__}: register\n" \
    #                                               f"Actual: {response.status_code}. Expected 200\n" \
    #                                               f"Message: {response.text}"
    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    # выводим данные текущего пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
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
    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"ПОСЛЕ обновления:\n {get_response.text}")
    # добавляем документ
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)
    # добавляем сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)
    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"ПОСЛЕ добавления документа и сэлфи:\n {get_response.text}")
