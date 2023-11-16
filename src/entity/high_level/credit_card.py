from dataclasses import dataclass

from src.entity.api_entity.credit_card.api_func_positive import \
    CreditCardApiFuncPositive
from src.entity.db_entity.credit_card.db_func import CreditCardDBFunc
from src.entity.high_level.data_func import Updatable


@dataclass
class CreditCardData(Updatable):
    """Основные данные по кредитной карте"""
    id: int = None
    user_id: int = None
    limit: int = None
    balance: bool = None
    active: bool = None
    exp_date: str = None


class CreditCard:
    def __init__(self, db_client, limit: int, user_id: int, user_auth_header: str):
        self.data = CreditCardData(limit=limit, user_id=user_id)
        self.auth_header = user_auth_header
        self.db_client = db_client

    def new(self):
        """Добавляем кредитную карту"""
        CreditCardApiFuncPositive.new(limit=self.data.limit, headers=self.auth_header)
        # в качестве id - берем последний id из таблицы
        self.data.id = CreditCardDBFunc.get_ids_by_user_id(self.db_client, self.data.user_id)[-1]
        self._update_data_from_server()

    def _update_data_from_server(self):
        """Обновляем данные credit_card (получаем данные с server-а)"""
        _data = CreditCardApiFuncPositive.get(headers=self.auth_header)
        self.data.update(_data)

    def increase_limit(self, limit: int):
        """Увеличиваем лимит credit_card"""
        _data = CreditCardApiFuncPositive.increase_limit(limit, headers=self.auth_header)
        self.data.update(_data)

    def close(self):
        """Закрываем credit_card"""
        CreditCardApiFuncPositive.close(headers=self.auth_header)
        self._update_data_from_server()

    def delete(self):
        """Удаляем credit_card"""
        CreditCardDBFunc.delete_by_id(self.db_client, self.data.id)
