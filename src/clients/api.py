"""
    Клиент для работы с API
"""
import requests

from src.clients.requests_kwargs_func import (convert_body_to_json,
                                              convert_url_to_str,
                                              separate_kwargs)


class ApiClient:
    """Класс-обертка для requests"""

    @staticmethod
    def post(**kwargs):
        """Отправляем POST запрос"""
        request_kwargs, other_kwargs = ApiClient._preprocess_kwargs(kwargs)
        response = requests.post(**request_kwargs)
        return response

    @staticmethod
    def put(**kwargs):
        """Отправляем PUT запрос"""
        request_kwargs, other_kwargs = ApiClient._preprocess_kwargs(kwargs)
        response = requests.put(**request_kwargs)
        return response

    @staticmethod
    def get(**kwargs):
        """Отправляем GET запрос"""
        request_kwargs, other_kwargs = ApiClient._preprocess_kwargs(kwargs)
        response = requests.get(**request_kwargs)
        return response

    @staticmethod
    def delete(**kwargs):
        """Отправляем DELETE запрос"""
        request_kwargs, other_kwargs = ApiClient._preprocess_kwargs(kwargs)
        response = requests.delete(**request_kwargs)
        return response

    @staticmethod
    def patch(**kwargs):
        """Отправляем PATCH запрос"""
        request_kwargs, other_kwargs = ApiClient._preprocess_kwargs(kwargs)
        response = requests.patch(**request_kwargs)
        return response

    @staticmethod
    def _preprocess_kwargs(kwargs):
        """Предобрабатываем kwargs для request-а"""
        convert_url_to_str(kwargs)
        # convert_body_to_json(kwargs)
        return separate_kwargs(kwargs)
