"""Общие переменные для всех тестов"""

from faker import Faker

# настраиваем кастомный faker
faker_ru = Faker("ru-RU")

# # для debug-а настраиваем const random seed
# Faker.seed(5)
# ModelFactory.seed_random = 5
