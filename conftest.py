import pytest
from helpers.register_new_courier import register_new_courier_and_return_login_password

@pytest.fixture
def new_courier():
    """
    Создаёт нового уникального курьера и возвращает его данные:
    { "login": ..., "password": ..., "firstName": ... }
    Если регистрация не удалась — пропускаем тест.
    """
    creds = register_new_courier_and_return_login_password()
    if not creds:
        pytest.skip("Не удалось зарегистрировать курьера (register_new_courier_and_return_login_password вернул пустой список)")
    return {"login": creds[0], "password": creds[1], "firstName": creds[2]}
