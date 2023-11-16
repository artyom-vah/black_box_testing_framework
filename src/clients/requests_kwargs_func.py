"""
    Функции для работы с kwargs для requests
"""
import inspect
import json
from enum import Enum

from requests.sessions import Session

# ключи, которые можно передавать в функции (get, post, put, delete) библиотеки requests
REQUESTS_FUNC_KEYS = inspect.getfullargspec(Session.request).args


def convert_body_to_json(kwargs):
    """Конвертируем body в json если нужно"""
    if kwargs.get("data") and isinstance(kwargs.get("data"), dict):
        kwargs["data"] = json.dumps(kwargs["data"])  # преобразуем объект в json-строку (по ключу "data")


def convert_url_to_str(kwargs):
    """Конвертируем URL в str если нужно"""
    if kwargs.get("url") and isinstance(kwargs.get("url"), Enum):
        kwargs["url"] = kwargs["url"].value


def separate_kwargs(kwargs):
    """Разделяем kwargs """
    set_kwargs = set(kwargs)
    kwargs_request_keys = set_kwargs.intersection(set(REQUESTS_FUNC_KEYS))  # ключи из kwargs для requests
    kwargs_other_keys = set_kwargs - kwargs_request_keys  # ключи из kwargs НЕ для requests
    request_kwargs = {key: kwargs[key] for key in kwargs_request_keys}  # kwargs для requests
    other_kwargs = {key: kwargs[key] for key in kwargs_other_keys}  # остальные kwargs
    return request_kwargs, other_kwargs


if __name__ == "__main__":
    kwargs = {"a": 1, "json": 5, "b": 3}
    request_kwargs, other_kwargs = separate_kwargs(kwargs)
    print(request_kwargs)
    print(other_kwargs)
