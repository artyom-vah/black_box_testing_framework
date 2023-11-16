import pytest

from src.entity.high_level.user import User
from tests.config import faker_ru


@pytest.mark.scenario
@pytest.mark.positive
def test_all_api(db_client):
    # данные для регистрации
    email = faker_ru.email()
    password = faker_ru.password()
    # создаем пользователя
    user2 = User(db_client, email, password)
    # регистрируем пользователя
    user2.register()
    # авторизируем пользователя
    user2.auth()
    # данные для обновления информации о пользователе
    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 40000,
        "another_loans": False,
        "birth_date": "1990-01-01",
        "sex": "male",
    }
    # обновляем информацию о пользователе
    user2.update(user_body)
    # добавляем документ
    user2.add_document_photo("rus_passport.jpg")
    # добавляем сэлфи
    user2.add_selfie_photo("jolie.jpg")
    # добавляем новую credit_card
    user2.add_credit_card()
    # пробуем увеличить лимит
    user2.credit_card.increase_limit(3000000)
    # закрываем credit_card
    user2.credit_card.close()
    # удаляем созданного пользователя
    user2.delete()
    db_client.close_connection()
