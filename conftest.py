import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import allure
from helpers.register_new_courier import (
    register_new_courier_and_return_login_password,
    login_and_get_id,
    delete_courier_by_id
)

@pytest.fixture(scope="session")
def courier_data():
    """Фикстура: создаёт тестового курьера, возвращает его данные и удаляет после тестов."""
    with allure.step("Регистрация тестового курьера"):
        creds = register_new_courier_and_return_login_password()
        assert creds, "Не удалось создать курьера через API"
        login, password, first_name = creds
        courier_id = login_and_get_id(login, password)
        yield {"login": login, "password": password, "first_name": first_name, "id": courier_id}

    with allure.step("Удаление тестового курьера"):
        if courier_id:
            delete_courier_by_id(courier_id) 
