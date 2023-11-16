"""
    Функции для "общей" обработки данных
"""
from json import JSONDecodeError

from requests import Response


def get_response_body(response: Response, err_msg):
    """Пытаемся получить body из response"""
    try:
        body = response.json()
    except JSONDecodeError:
        raise TypeError(f"{err_msg}: response body НЕ JSON!")
    return body


def find_dict_in_list_by_key_value(key, value, dict_list):
    """Ищем в списке словарей по dict[key] == value"""
    return list(filter(lambda _dict: _dict[key] == value, dict_list))
