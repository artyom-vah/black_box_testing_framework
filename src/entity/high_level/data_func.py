"""
    Функции для работы с данными
"""


class Updatable:
    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)
