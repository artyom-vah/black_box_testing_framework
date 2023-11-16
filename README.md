# Автотесты для приложения [CreditCardShift](https://gitlab.com/shift-python-qa/y2023/materials/credit_card_shift)

## Задание:




Написать автотесты для API сервиса **credit_card_shift**. Сценарии можно посмотреть в требованиях и придумать свои дополнительные.

Не забудьте создать красочное README и подробный CONTRIBUTING, а также создать запрос на слияние (МР).

### Дополнительные требования по реализации:

- **Валидация body у response:** Используйте **pydantic** для валидации тела ответа.

- **Запуск тестов на разных окружениях:** Реализуйте запуск тестов на разных окружениях с помощью различных файлов `.env` и прокидывания типа окружения в `pytest`.

- **Практика "разворачивания с нуля":** Для практики "разворачивания с нуля" рекомендуется покрыть тестами сервис **petstore** и выгрузить его в отдельный репозиторий.

## Структура проекта

- **src**: В этой папке находится вспомогательный код (микро-фреймворк) для более удобного написания тестов.

    - **clients**: Здесь реализованы клиенты для работы с API и базой данных.
    
    - **entity**: Эта директория содержит абстракции для сущностей **User** и **CreditCard** на различных уровнях:

        - **db_entity**: Абстракции на уровне базы данных.
        
        - **api_entity**: Абстракции на уровне API. В файлах `api_func.py` находятся "тонкие" обертки для каждой сущности вокруг API-клиента, рекомендуется использовать их для **негативных** проверок.

        - **api_func_positive.py**: Обертки вокруг `api_func.py`, которые следует использовать для более _тонкой_ проверки **позитивных** сценариев.

        - **high_level**: Высокоуровневые абстракции, автоматизирующие рутинную работу. Используют как [api_entity](src/entity/api_entity), так и [db_entity](src/entity/db_entity). Рекомендуется использовать данный код для сценарных проверок и создания предусловий более низкоуровневых тестов.

    - **config.py**: В этом файле осуществляется загрузка переменных среды из файла `.env`.

- **tests**: В этой папке хранятся файлы с тестами.

    - **data**: Тестовые данные с фотографиями документов и сэлфи.

- **setup.cfg**: Настройки для запуска тестов с помощью pytest.

Почти в каждом .py файле в конце есть секция "if __name__ == __main__", где приведен тестовый код для конкретного файла. Рекомендуется ознакомиться с этим функционалом и провести эксперименты.



## **Стек**
[![Python Version](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/downloads/release/python-3110/)

## **Дополнительные библиотеки**
[![Requests Version](https://img.shields.io/badge/Requests-2.31.0-brightgreen)](https://pypi.org/project/requests/2.31.0/)
[![Pytest Version](https://img.shields.io/badge/Pytest-7.4.2-red)](https://pypi.org/project/pytest/7.4.2/)
[![Faker Version](https://img.shields.io/badge/Faker-19.10.0-yellow)](https://pypi.org/project/faker/19.10.0/)
[![Isort Version](https://img.shields.io/badge/Isort-5.12.0-orange)](https://pypi.org/project/isort/5.12.0/)
[![Python-Dotenv Version](https://img.shields.io/badge/Python--Dotenv-1.0.0-lightgrey)](https://pypi.org/project/python-dotenv/1.0.0/)

### Структура тестов:
```
tests/
|-- my_scenarios/
| |-- __init__.py
| |-- test_algorithm_calculating_available_credit_limit.py
| |-- test_all_api.py
| |-- test_four.py
| |-- test_one.py 
| |-- test_three.py
| |-- test_two.py
```

### Структура проекта файлов:
### <div style="color: green">  Сценарий 1: Регистрация и авторизация ```модуль test_one.py ```</div>

**Основной сценарий:**
1. Пользователь, который впервые посещает сервис CreditCard, регистрируется.
2. После успешной регистрации, пользователь проходит авторизацию.

**Альтернативы:**
- **Сценарий 5a:** Пользователь уже зарегистрирован в базе данных БКК.
- **Сценарии 5b и 7a:** Введенный email не соответствует формату.
- **Сценарии 5c и 7b:** Введенный пароль не соответствует формату.

### <div style="color: green"> Сценарий 2: Открытие новой кредитной карты ```модуль test_two.py ```

**Основной сценарий:**
1. Клиент банка решает открыть новую кредитную карту в сервисе CreditCard.

**Альтернативы:**
- **Сценарий 8a:** Токен авторизации устарел при получении запроса PATCH /user.
- **Сценарий 8b:** Ошибка при обновлении данных пользователя запросом PATCH /user.
- **Сценарий 10a:** Токен авторизации устарел при получении запроса POST /user/document.
- **Сценарий 11b:** Фотография документа не прошла валидацию в Фотосервисе.
- **Сценарий 14a:** Токен авторизации устарел при получении запроса POST /user/face.
- **Сценарий 15b:** Фотография сэлфи не прошла валидацию в Фотосервисе.
- **Сценарий 19a:** Токен авторизации устарел при получении запроса POST /credit_card/new.
- **Сценарий 20a:** У пользователя уже есть открытая кредитная карта в базе данных.

### <div style="color: green">   Сценарий 3: Увеличение лимита по карте ```модуль test_three.py ```

**Основной сценарий:**
1. Клиент банка с открытой кредитной картой решает увеличить лимит по карте.

**Более подробный вариант сценария 3:**
1. Клиент банка с открытой кредитной картой хочет увеличить лимит по карте.

**Альтернативы:**
- **Сценарий 2a:** Токен авторизации устарел при получении запроса GET /credit_card.
- **Сценарий 9a:** Токен авторизации устарел при получении запроса GET /user.
- **Сценарии 11a, 11b, 11c:** Различные сценарии, связанные с отсутствием проверенных фотографий и документов.
- **Сценарий 13a:** Токен авторизации устарел при получении запроса POST /credit_card/increase_limit.
- **Сценарии 15a и 17a:** Сценарии, связанные с текущим лимитом по карте.

### <div style="color: green">   Сценарий 4: Закрытие кредитной карты ```test_four.py```

**Основной сценарий:**
1. Клиент банка с открытой кредитной картой решает закрыть карту.

**Альтернативы:**
- **Сценарий 2a:** Токен авторизации устарел при получении запроса GET /user.
- **Сценарии 7a и 7a (по сложному):** Токен авторизации устарел при получении запроса POST /credit_card/close.

#### <div style="color: green">  Требования к БКК 11: Расчет доступного кредитного лимита

Тут находится основная функциональность данного сервиса. Всего 17 вариантов расчета, см. таблицу принятия решений. ```test_algorithm_calculating_available_credit_limit.py```

**Автор проекта: Артем Вахрушев.**



