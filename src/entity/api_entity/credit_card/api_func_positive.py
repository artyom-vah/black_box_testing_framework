"""
    API-функции для работы с сущностью credit_card - для ПОЗИТИВНЫХ сценариев
    В каждой функции сразу проверяется статус код response и возвращается отформатированное значение (если нужно)
"""
from http import HTTPStatus

from src.data_func import get_response_body
from src.entity.api_entity.credit_card.api_func import CreditCardApiFunc


class CreditCardApiFuncPositive:
    err_msg_template = lambda func_name: f"{CreditCardApiFuncPositive.__name__}:{func_name}"

    @staticmethod
    def new(limit: int, **kwargs):
        """Добавляем кредитную карту"""
        limit_params = {"limit": limit}
        response = CreditCardApiFunc.new(limit_params, **kwargs)
        err_msg_template = CreditCardApiFuncPositive.err_msg_template(CreditCardApiFuncPositive.new.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"
        body = get_response_body(response, err_msg=f"{err_msg_template}")
        return body

    @staticmethod
    def increase_limit(limit: int, **kwargs):
        """Увеличиваем лимит кредитной карты"""
        limit_params = {"limit": limit}
        response = CreditCardApiFunc.increase_limit(limit_params, **kwargs)
        err_msg_template = CreditCardApiFuncPositive.err_msg_template(CreditCardApiFuncPositive.increase_limit.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"
        body = get_response_body(response, err_msg=f"{err_msg_template}")
        return body

    @staticmethod
    def get(**kwargs):
        """Получаем данные кредитной карты"""
        response = CreditCardApiFunc.get(**kwargs)
        err_msg_template = CreditCardApiFuncPositive.err_msg_template(CreditCardApiFuncPositive.get.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"
        body = get_response_body(response, err_msg=f"{err_msg_template}")
        return body

    @staticmethod
    def close(**kwargs):
        """Закрываем кредитную карту"""
        response = CreditCardApiFunc.close(**kwargs)
        err_msg_template = CreditCardApiFuncPositive.err_msg_template(CreditCardApiFuncPositive.get.__name__)
        assert response.status_code == HTTPStatus.OK, f"Wrong status_code on {err_msg_template}"


if __name__ == "__main__":
    from entity.api_entity.user.api_func import UserApiFunc
    from entity.api_entity.user.data_func import UserDataFunc

    # данные для авторизации
    credential_form = {
        "username": "test1@mail.ru",
        "password": "password"
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(credential_form)
    # заводим новую кредитную карту
    limit_params = {"limit": 1000000}
    _body = CreditCardApiFuncPositive.new(limit_params, headers=auth_headers)
    print("Новая кредитная карта:")
    print(_body)
    # увеличиваем лимит по карте
    limit_params = {"limit": 3000000}
    # добавляем документ - чтобы корректно увеличить лимит
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)
    _body = CreditCardApiFuncPositive.increase_limit(limit_params, headers=auth_headers)
    print("Обновленная кредитная карта:")
    print(_body)
    # закрываем кредитную карту
    CreditCardApiFuncPositive.close(headers=auth_headers)
    # получаем информацию по карте
    _body = CreditCardApiFuncPositive.get(headers=auth_headers)
    print("Удаленная кредитная карта:")
    print(_body)
