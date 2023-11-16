'''
Требования к БКК 11. Реализовать алгоритм расчета доступного кредитного лимита:

Всего 17 вариантов расчета, см. таблицу принятия решений и чек-лист требование 11.
'''
import pytest

from src.entity.api_entity.credit_card.api_func import CreditCardApiFunc
from src.entity.api_entity.user.api_func import UserApiFunc
from src.entity.api_entity.user.data_func import UserDataFunc
from tests.conftest import faker_ru


@pytest.mark.skip
def test_one():
    """
    Пол: Мужчина (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: 100 000 <= доход < 300 000 (+10 000)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 30 000 руб.

    Запрошенный лимит: 55 000
    ОР: клиенту доступен КЛ в размере 30 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 150_000_00,
        "another_loans": True,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
        "sex": "male",
    }

    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем фото-сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 55_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 30_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_two():
    """
    Пол: Женщина (+40 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: Нет (+0)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИО (+5 000)
    Фото ДУЛ: Да, невалидное (+0)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 55 000 руб.

    Запрошенный лимит: 100 000
    ОР: клиенту доступен КЛ в размере 55 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Петрова Вера Борисовна",
        "income": 0,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, Нет (+0)
        "sex": "female",
    }

    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)

    # добавляем документ фото дул невалидное
    document_file = UserDataFunc.get_document_file("demo.txt")
    UserApiFunc.document(document_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 100_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 55_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_three_1():
    """
    Пол: Не указано (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: Нет (+0)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 22 000 руб.

    Запрошенный лимит: 20 000
    ОР: клиенту доступен КЛ в размере 20 000 руб.
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 0,
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
    }
    UserApiFunc.update(user_body=user_body, headers=auth_headers)  # обновляем информацию о пользователе
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 20_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 20_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_three_2():
    """
    Пол: Не указано (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: Нет (+0)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 22 000 руб.

    Запрошенный лимит: 22 000
    ОР: клиенту доступен КЛ в размере 22 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 0,
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
    }
    UserApiFunc.update(user_body=user_body, headers=auth_headers)  # обновляем информацию о пользователе
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 22_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 22_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_four_1():
    """
    Пол: Мужчина (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: >=300 000 (+100 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Да, невалидное (+0)

    Доступный кредитный лимит 142 000 руб.

    Запрошенный лимит: 150 000
    ОР: клиенту доступен КЛ в размере 142 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 305_000_00,
        "another_loans": False,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "male",
    }
    UserApiFunc.update(user_body=user_body, headers=auth_headers)  # обновляем информацию о пользователе
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи невалидное
    face_file = UserDataFunc.get_face_file("demo.txt")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 150_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 142_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_four_2():
    """
    Пол: Мужчина (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: >=300 000 (+100 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Да, невалидное (+0)

    Доступный кредитный лимит 142 000 руб.

    Запрошенный лимит: 130 000
    ОР: клиенту доступен КЛ в размере 130 000 руб.
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 305_000_00,
        "another_loans": False,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "male",
    }
    UserApiFunc.update(user_body=user_body, headers=auth_headers)  # обновляем информацию о пользователе
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи невалидное
    face_file = UserDataFunc.get_face_file("demo.txt")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 130_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 130_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_five():
    """
    Пол: Женщина (+40 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: >= 300 000 (+100 000)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 132 000 руб.

    Запрошенный лимит: 200 000 руб.
    ОР: клиенту доступен КЛ в размере 132 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 301_000_00,
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "female",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 200_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    # проверка доступного кредитного лимита
    exp_res = 132_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_six():
    """
    Пол: Не указано (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: >= 300 000 (+100 000)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Да, ФИО (+5 000)
    Фото ДУЛ: Да, невалидное (+0)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 122 000 руб.

    Запрошенный лимит: 120 000 руб.
    ОР: клиенту доступен КЛ в размере 122 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 301_000_00,
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул невалидное
    document_file = UserDataFunc.get_document_file("demo.txt")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 120_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 120_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_seven_1():
    """
    Пол: Не указано (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: < 100 000 (+1 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 41 000 руб.

    Запрошенный лимит: 40 000 руб.
    ОР: клиенту доступен КЛ в размере 40 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван",
        "income": 95_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул валидное
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 40_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 40_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_seven_2():
    """
    Пол: Не указано (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: < 100 000 (+1 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 41 000 руб.

    Запрошенный лимит: 35 000 руб.
    ОР: клиенту доступен КЛ в размере 35 000 руб.
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван",
        "income": 95_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул валидное
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 35_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 35_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_eight():
    """
    Пол: Женщина (+40 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: 100 000 <= доход < 300 000 (+10 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Да, невалидное (+0)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 60 000 руб.

    Запрошенный лимит: 80 000 руб.
    ОР: клиенту доступен КЛ в размере 60 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 200_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
        "sex": "female",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул валидное невалидное
    document_file = UserDataFunc.get_document_file("demo.txt")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи невалидное
    face_file = UserDataFunc.get_face_file("demo.txt")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 80_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 60_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_nine():
    """
    Пол: Мужчина (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: < 100 000 (+1 000)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Да, ФИО (+5 000)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Да, невалидное (+0)

    Доступный кредитный лимит 18 000 руб.

    Запрошенный лимит: 10 000 руб.
    ОР: клиенту доступен КЛ в размере 10 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "income": 90_000_00,
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "male",
    }
    # обновляем информацию о пользователе невалидное
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем фото-сэлфи невалидное
    face_file = UserDataFunc.get_face_file("demo.txt")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 10_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 20_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_ten_1():
    """
    Пол: Мужчина (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: < 100 000 (+1 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Да, невалидное (+0)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 36 000 руб.

    Запрошенный лимит: 30 000 руб.
    ОР: клиенту доступен КЛ в размере 30 000 руб.
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 90_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
        "sex": "male",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул невалидное
    document_file = UserDataFunc.get_document_file("demo.txt")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи валидное
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 30_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 30_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_ten_2():
    """
    Пол: Мужчина (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: < 100 000 (+1 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Да, невалидное (+0)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 36 000 руб.

    Запрошенный лимит: 40 000 руб.
    ОР: клиенту доступен КЛ в размере 36 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 90_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
        "sex": "male",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул невалидное
    document_file = UserDataFunc.get_document_file("demo.txt")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи валидное
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 40_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 36_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_eleven():
    """
    Пол: Женщина (+40 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: 100 000 <= доход < 300 000 (+10 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 77 000 руб.

    Запрошенный лимит: 80 000 руб.
    ОР: клиенту доступен КЛ в размере 77 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Петрова Вера",
        "income": 200_000_00,
        "another_loans": False,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "female",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул валидное
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи валидное
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 80_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 77_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_twelve():
    """
    Пол: Женщина (+40 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: Доход < 100 000 (+1 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, невалидное (+5 000)
    Фото селфи: Да, невалидное (+5 000)

    Доступный кредитный лимит 58 000 руб.

    Запрошенный лимит: 70 000 руб.
    ОР: клиенту доступен КЛ в размере 58 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Петрова Вера",
        "income": 80_000_00,
        "another_loans": False,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "female",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул невалидное
    document_file = UserDataFunc.get_document_file("demo.txt")
    UserApiFunc.document(document_file, headers=auth_headers)

    # добавляем фото-сэлфи невалидное
    face_file = UserDataFunc.get_face_file("demo.txt")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 70_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 58_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_thirteen_1():
    """
    Пол: Мужчина (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: Нет (+0)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИО (+5 000)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 35 000.

    Запрошенный лимит: 40 000 руб.
    ОР: клиенту доступен КЛ в размере 35 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
        "sex": "male",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 40_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 35_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_thirteen_2():
    """
    Пол: Мужчина (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: Нет (+0)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИО (+5 000)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 35 000.

    Запрошенный лимит: 30 000 руб.
    ОР: клиенту доступен КЛ в размере 30 000 руб.
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван Иванович",
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
        "sex": "male",
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 30_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 30_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_fourteen():
    """
    Пол: Не указано (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: Нет (+0)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Да, невалидное (+0)

    Доступный кредитный лимит 17 000 руб.

    Запрошенный лимит: 10 000 руб.
    ОР: клиенту доступен КЛ в размере 20 000 руб.
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван",
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем фото-сэлфи невалидное
    face_file = UserDataFunc.get_face_file("demo.txt")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 10_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 20_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_fiveteen():
    """
    Пол: Не указано (+20 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: 100 000 <= доход < 300 000 (+10 000)
    Наличие кредитов: Да (-10 000)
    Указал ФИО: Да, ФИО (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 32 000 руб.

    Запрошенный лимит: 40 000 руб.
    ОР: клиенту доступен КЛ в размере 32 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Иванов Иван",
        "income": 120_000_00,
        "another_loans": True,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул валидное
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 40_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 32_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


def test_sixteen_1():
    """
    Пол: Не указано (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: >=300 000 (+100 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 135 000 руб.

    Запрошенный лимит: 90 000 руб.
    ОР: клиенту доступен КЛ в размере 90 000 руб.

    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 305_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем фото-сэлфи
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 135_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 135_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_sixteen_2():
    """
    Пол: Не указано (+20 000)
    Возраст: 45 <= возраст <= 65 (+0)
    Доход: >=300 000 (+100 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Нет (+0)
    Фото ДУЛ: Нет (+0)
    Фото селфи: Да, валидное (+5 000)

    Доступный кредитный лимит 135 000 руб.

    Запрошенный лимит: 150 000 руб.
    ОР: клиенту доступен КЛ в размере 135 000 руб.

    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }

    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "income": 305_000_00,
        "another_loans": False,
        "birth_date": "1973-01-01",  # 50 лет, 45 <= возраст <= 65 (+0)
    }
    # обновляем информацию о пользователе
    UserApiFunc.update(user_body=user_body, headers=auth_headers)
    UserApiFunc.get(headers=auth_headers)

    # добавляем фото-сэлфи валидное
    face_file = UserDataFunc.get_face_file("jolie.jpg")
    UserApiFunc.face(face_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 150_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 135_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")


@pytest.mark.skip
def test_seventeen():
    """
    Пол: Женщина (+40 000)
    Возраст: 18 <= возраст < 45 (+2 000)
    Доход: 100 000 <= доход < 300 000 (+10 000)
    Наличие кредитов: Нет (+10 000)
    Указал ФИО: Да, ФИ (+5 000)
    Фото ДУЛ: Да, валидное (+5 000)
    Фото селфи: Нет (+0)

    Доступный кредитный лимит 72 000 руб.

    Запрошенный лимит: 100 000
    ОР: клиенту доступен КЛ в размере 72 000 руб.
    тест - Failed
    """

    # данные для регистрации
    credential_body = {
        "email": faker_ru.email(),
        "password": faker_ru.password()
    }
    UserApiFunc.register(credential_body)

    # данные для авторизации
    user_form = {
        "username": credential_body["email"],
        "password": credential_body["password"]
    }
    # получаем header-ы авторизации
    auth_headers = UserDataFunc.get_auth_header(user_form)
    UserApiFunc.get(headers=auth_headers)

    user_body = {
        "full_name": "Петрова Вера",
        "income": 150_000_00,
        "another_loans": False,
        "birth_date": "1990-01-01",  # 33 года, 18 <= возраст < 45 (+2 000)
        "sex": "female",
    }
    UserApiFunc.update(user_body=user_body, headers=auth_headers)  # обновляем информацию о пользователе
    UserApiFunc.get(headers=auth_headers)

    # добавляем документ фото дул
    document_file = UserDataFunc.get_document_file("rus_passport.jpg")
    UserApiFunc.document(document_file, headers=auth_headers)

    # заводим новую кредитную карту с лимитом
    limit_params = {"limit": 100_000_00}
    _response = CreditCardApiFunc.new(limit_params, headers=auth_headers)

    # проверка доступного кредитного лимита
    exp_res = 72_000_00
    assert _response.json()['limit'] == exp_res, f"Expected {exp_res}, but received {_response.json()['limit']}"

    # выводим данные обновленного пользователя
    get_response = UserApiFunc.get(headers=auth_headers)
    print(f"Данные пользователя ПОСЛЕ обновления:\n {get_response.text}")

    # выводим данные о новой КК
    _response = CreditCardApiFunc.get(headers=auth_headers)
    print(f"Заведенная кредитная карта:\n{_response.text}")
