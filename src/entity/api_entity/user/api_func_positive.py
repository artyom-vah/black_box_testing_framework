"""
    API-функции для работы с сущностью user - для ПОЗИТИВНЫХ сценариев
    В каждой функции сразу проверяется статус код response и возвращается отформатированное значение (если нужно)
"""
from http import HTTPStatus

from src.data_func import get_response_body
from src.entity.api_entity.user.api_func import UserApiFunc


class UserApiFuncPositive:
    err_msg_template = lambda func_name: f"{UserApiFuncPositive.__name__}:{func_name}"

    # TODO заиспользовать декоратор
    @staticmethod
    def register(credential_body: dict, **kwargs):
        """Регистрируем user-а"""
        response = UserApiFunc.register(credential_body, **kwargs)
        err_msg_template = UserApiFuncPositive.err_msg_template(UserApiFuncPositive.register.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"

    @staticmethod
    def auth(credential_form: dict, **kwargs):
        """Авторизуем user-а"""
        response = UserApiFunc.auth(credential_form, **kwargs)
        err_msg_template = UserApiFuncPositive.err_msg_template(UserApiFuncPositive.auth.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"
        body = get_response_body(response, err_msg=f"{err_msg_template}")
        return body

    @staticmethod
    def get(**kwargs):
        """Получаем текущего user-а"""
        response = UserApiFunc.get(**kwargs)
        err_msg_template = UserApiFuncPositive.err_msg_template(UserApiFuncPositive.get.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"
        body = get_response_body(response, err_msg=f"{err_msg_template}")
        return body

    @staticmethod
    def update(user_body: dict, **kwargs):
        """Обновляем текущего user-а"""
        response = UserApiFunc.update(user_body, **kwargs)
        err_msg_template = UserApiFuncPositive.err_msg_template(UserApiFuncPositive.update.__name__)
        assert response.status_code == HTTPStatus.NO_CONTENT, f"Wrong status_code on {err_msg_template}"

    @staticmethod
    def document(files, **kwargs):
        """Отправляем фото документа user-а"""
        response = UserApiFunc.document(files, **kwargs)
        err_msg_template = UserApiFuncPositive.err_msg_template(UserApiFuncPositive.document.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"

    @staticmethod
    def face(files, **kwargs):
        """Отправляем фото сэлфи user-а"""
        response = UserApiFunc.face(files, **kwargs)
        err_msg_template = UserApiFuncPositive.err_msg_template(UserApiFuncPositive.document.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"


if __name__ == "__main__":
    from entity.api_entity.user.data_func import UserDataFunc

    # данные для регистрации
    credential_body = {
        "email": "test1@mail.ru",
        "password": "password"
    }
    # # регистрируем пользователя
    # response = UserApiFuncPositive.register(credential_body)
    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    # выводим данные текущего пользователя
    response_body = UserApiFuncPositive.get(headers=auth_headers)
    print(f"ДО обновления:\n {response_body}")
    # данные для обновления информации о пользователе
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    UserApiFuncPositive.update(user_body=user_body, headers=auth_headers)
    # выводим данные обновленного пользователя
    response_body = UserApiFuncPositive.get(headers=auth_headers)
    print(f"ПОСЛЕ обновления:\n {response_body}")
    # добавляем документ
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFuncPositive.document(document_file, headers=auth_headers)
    # добавляем сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFuncPositive.face(face_file, headers=auth_headers)
    # выводим данные обновленного пользователя
    response_body = UserApiFuncPositive.get(headers=auth_headers)
    print(f"ПОСЛЕ добавления документа и сэлфи:\n {response_body}")
