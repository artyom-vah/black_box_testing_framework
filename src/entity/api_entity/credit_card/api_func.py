"""
    API-функции для работы с сущностью credit_card
"""

from src.clients.api import ApiClient
from src.entity.api_entity.credit_card.api_path import CreditCardFullPath


class CreditCardApiFunc:
    @staticmethod
    def new(limit_params: dict, **kwargs):
        """Добавляем кредитную карту"""
        return ApiClient.post(url=CreditCardFullPath.new, params=limit_params, **kwargs)

    @staticmethod
    def increase_limit(limit_params: dict, **kwargs):
        """Увеличиваем лимит кредитной карты"""
        return ApiClient.post(url=CreditCardFullPath.increase_limit, params=limit_params, **kwargs)

    @staticmethod
    def get(**kwargs):
        """Получаем данные кредитной карты"""
        return ApiClient.get(url=CreditCardFullPath.get, **kwargs)

    @staticmethod
    def close(**kwargs):
        """Закрываем кредитную карту"""
        return ApiClient.post(url=CreditCardFullPath.close, **kwargs)


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
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)
    print("Новая кредитная карта:")
    print(_response.text)
    # увеличиваем лимит по карте
    limit_params = {"limit": 3000000}
    # добавляем документ - чтобы корректно увеличить лимит
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)
    _response = CreditCardApiFunc.increase_limit(limit_params, headers=auth_headers)
    print("Обновленная кредитная карта:")
    print(_response.text)
    # закрываем кредитную карту
    CreditCardApiFunc.close(headers=auth_headers)
    # получаем информацию по карте
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print("Удаленная кредитная карта:")
    print(_response.text)
