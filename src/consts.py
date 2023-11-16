"""
    Константы
"""

import os
from enum import auto

from strenum import StrEnum

# находим абсолютный путь до корня проекта
curr_dir = os.path.dirname(__file__)
ROOT_PATH = os.path.join(curr_dir, '..')

TEST_FOLDER = "tests"
DATA_FOLDER = "data"
DOCUMENT_FOLDER = "document"
FACE_FOLDER = "face"

STANDART_LIMIT = 2_000_000  # лимит credit_card - устанавливаемый по-умолчанию
INVALID_TOKEN = {'Authorization': 'Bearer 123'}

def get_document_file_path(document_name):
    return os.path.join(ROOT_PATH, TEST_FOLDER, DATA_FOLDER, DOCUMENT_FOLDER, document_name)


def get_face_file_path(face_name):
    return os.path.join(ROOT_PATH, TEST_FOLDER, DATA_FOLDER, FACE_FOLDER, face_name)


class EnvName(StrEnum):
    """Названия ENV переменных в файле .env"""
    # base_url
    CREDIT_CARD_URL = auto()
    # DB credentials
    DB_NAME = auto()
    DB_USER = auto()
    DB_PASSWORD = auto()
    DB_HOST = auto()
    DB_PORT = auto()
    # user1 credentials
    USER1_EMAIL = auto()
    USER1_PASSWORD = auto()
