"""
    API-пути для данной сущности
"""
from enum import Enum

from strenum import StrEnum

from src.config import base_url
from src.entity.api_entity.credit_card import entity_name


class CreditCardPath(StrEnum):
    """Локальные пути"""
    new = f"{entity_name}/new"
    increase_limit = f"{entity_name}/increase_limit"
    get = f"{entity_name}"
    close = f"{entity_name}/close"


class CreditCardFullPath(Enum):
    """Полные пути"""
    new = base_url / CreditCardPath.new
    increase_limit = base_url / CreditCardPath.increase_limit
    get = base_url / CreditCardPath.get
    close = base_url / CreditCardPath.close


if __name__ == "__main__":
    # для теста
    print(CreditCardFullPath.new.value)  # так как тип Enum - для получения значения необходимо писать .value
    print(CreditCardFullPath.increase_limit.value)
    print(CreditCardFullPath.get.value)
    print(CreditCardFullPath.close.value)
