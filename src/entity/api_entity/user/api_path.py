"""
    API-пути для данной сущности
"""
from enum import Enum

from strenum import StrEnum

from src.config import base_url
from src.entity.api_entity.user import entity_name


class UserPath(StrEnum):
    """Локальные пути"""
    register = f"{entity_name}/register"
    auth = f"auth/access_token"
    get = f"{entity_name}"
    patch = f"{entity_name}"
    document = f"{entity_name}/document"
    face = f"{entity_name}/face"


class UserFullPath(Enum):
    """Полные пути"""
    register = base_url / UserPath.register
    auth = base_url / UserPath.auth
    get = base_url / UserPath.get
    patch = base_url / UserPath.patch
    document = base_url / UserPath.document
    face = base_url / UserPath.face


if __name__ == "__main__":
    # для теста
    print(UserFullPath.register.value)  # так как тип Enum - для получения значения необходимо писать .value
    print(UserFullPath.get.value)
    print(UserFullPath.patch.value)
    print(UserFullPath.document.value)
    print(UserFullPath.face.value)
    print(UserFullPath.auth.value)
