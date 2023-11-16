"""
    Функции для работы с данными
"""


def create_values_for_insert(in_data: dict):
    """Формируем строку для блока VALUES в INSERT запросе"""
    values_str = ""
    for value in in_data.values():
        if isinstance(value, str):
            values_str += f"'{value}', "
        elif isinstance(value, int):
            values_str += f"{value}, "
    return values_str[:-2]


def create_set_for_update(in_data: dict):
    """Формируем строку из user_data для блока SET в UPDATE запросе"""
    set_str = ""
    for key, value in in_data.items():
        if isinstance(value, str):
            set_str += f"{key}='{value}', "
        elif isinstance(value, int):
            set_str += f"{key}={value}, "
    return set_str[:-2]
