"""
    Конфигурационный файл
"""

import os

from dotenv import load_dotenv
from yarl import URL

from src.consts import EnvName

load_dotenv()  # загружаем все env-переменные из .env файла

# CREDIT_CARD_URL
_url_str = os.getenv(EnvName.CREDIT_CARD_URL)
base_url = URL(_url_str)

if __name__ == "__main__":
    # для теста
    print(base_url)
