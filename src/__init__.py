import pytest

# для того чтобы нормально отображались ошибки в assert-ах (traceback)
# тк assert-ы лежат вне test_ функции
pytest.register_assert_rewrite('src.entity.high_level.user')
