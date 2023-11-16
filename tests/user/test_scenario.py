"""Сценарные тесты user"""

import pytest

from src.consts import STANDART_LIMIT


@pytest.mark.scenario
@pytest.mark.positive
@pytest.mark.parametrize('simple_user', [("test2@mail.ru", "password")], indirect=True)
def test_simple_scenario(simple_user):
    """Простой сценарный тест для user"""
    # данные для обновления информации о пользователе
    update_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    simple_user.update(update_body)
    # проверяем что все обновилось корректно
    simple_user.compare_data_with_dict(update_body, "Error on UPDATE User")
    # добавляем документ
    simple_user.add_document_photo("rus_passport.jpg")
    assert simple_user.data.status_document, "Wrong status_document"
    # добавляем сэлфи
    simple_user.add_selfie_photo("jolie.jpg")
    assert simple_user.data.status_face, "Wrong status_document"
    # добавляем новую credit_card
    simple_user.add_credit_card()
    assert simple_user.credit_card.data.limit == STANDART_LIMIT
    # пробуем увеличить лимит
    simple_user.credit_card.increase_limit(3_000_000)
    assert simple_user.credit_card.data.limit == 3_000_000
    # закрываем credit_card
    simple_user.credit_card.close()
    assert not simple_user.credit_card.data.active
