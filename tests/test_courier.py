import pytest
import requests
import allure
from helpers.register_new_courier import (
    generate_random_string,
    register_new_courier_and_return_login_password,
    login_and_get_id,
    delete_courier_by_id
)
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER


@allure.feature("Курьеры")
@allure.story("Создание нового курьера")
def test_create_courier_success():
    login, password, first_name = register_new_courier_and_return_login_password()
    assert login and password, "Не удалось зарегистрировать курьера"

    with allure.step("Авторизация созданного курьера"):
        courier_id = login_and_get_id(login, password)
        assert isinstance(courier_id, int), "ID курьера не получен"

    with allure.step("Удаление курьера после теста"):
        assert delete_courier_by_id(courier_id)


@allure.feature("Курьеры")
@allure.story("Создание дублирующего курьера")
def test_create_duplicate_courier_fails():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {"login": login, "password": password, "firstName": first_name}
    r1 = requests.post(CREATE_COURIER, json=payload)
    assert r1.status_code == 201

    with allure.step("Попытка создать курьера с тем же логином"):
        r2 = requests.post(CREATE_COURIER, json=payload)
        assert r2.status_code in (400, 409), f"Ожидался 400/409, получили {r2.status_code}"

    courier_id = login_and_get_id(login, password)
    if courier_id:
        delete_courier_by_id(courier_id)


@pytest.mark.parametrize("missing_field,payload", [
    ("login", {"password": "pass", "firstName": "Ivan"}),
    ("password", {"login": "user", "firstName": "Ivan"}),
    ("firstName", {"login": "user", "password": "pass"})
])
@allure.feature("Курьеры")
@allure.story("Создание курьера без обязательных полей")
def test_create_courier_missing_field_returns_error(missing_field, payload):
    r = requests.post(CREATE_COURIER, json=payload)
    assert r.status_code == 400, f"Ожидался 400 при отсутствии поля {missing_field}"
    assert "message" in r.text or r.text, "Ожидалось сообщение об ошибке"


@allure.feature("Курьеры")
@allure.story("Авторизация курьера")
def test_login_courier_success(courier_data):
    with allure.step("Авторизация с валидными данными"):
        payload = {"login": courier_data["login"], "password": courier_data["password"]}
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 200
        assert "id" in r.json()


@allure.feature("Курьеры")
@allure.story("Авторизация с неверными данными")
def test_login_with_wrong_credentials_returns_error():
    payload = {"login": "wrong_user", "password": "wrong_pass"}
    r = requests.post(LOGIN_COURIER, json=payload)
    assert r.status_code in (400, 404)
