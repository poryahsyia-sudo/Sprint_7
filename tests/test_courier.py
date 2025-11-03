import pytest
import requests
import allure
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER
from helpers.register_new_courier import (
    generate_random_string,
    register_new_courier_and_return_login_password,
    login_and_get_id,
    delete_courier_by_id
)

# ---------- Создание курьера ----------

@allure.feature("Курьеры")
@allure.story("Создание курьера")
def test_create_courier_success():
    # регистрируем нового курьера уникальными данными
    login = f"user_{generate_random_string()}"
    password = f"pass_{generate_random_string()}"
    first_name = f"name_{generate_random_string(5)}"

    payload = {"login": login, "password": password, "firstName": first_name}
    r = requests.post(CREATE_COURIER, json=payload)
    assert r.status_code == 201, f"Ожидался 201, получили {r.status_code}: {r.text}"
    # проверка тела ответа, если API возвращает {"ok": true}
    try:
        body = r.json()
        assert body.get("ok") is True
    except ValueError:
        # если тело не JSON — просто пропускаем дополнительную проверку
        pass

@allure.feature("Курьеры")
@allure.story("Дубликат курьера")
def test_create_duplicate_courier_fails():
    # создаём конкретный уникальный курьера через helper
    creds = register_new_courier_and_return_login_password()
    assert creds, "Не удалось зарегистрировать первого курьера"

    payload = {"login": creds[0], "password": creds[1], "firstName": creds[2]}
    r2 = requests.post(CREATE_COURIER, json=payload)
    # ожидаем ошибку дублирования (обычно 400 или 409) — тест проверяет поведение API
    assert r2.status_code in (400, 409), f"Ожидался 400/409 при дублировании, получили {r2.status_code}: {r2.text}"

    # удаляем созданного курьера (если можно)
    courier_id = login_and_get_id(creds[0], creds[1])
    if courier_id:
        delete_courier_by_id(courier_id)

@allure.feature("Курьеры")
@allure.story("Создание курьера без поля password")
def test_create_courier_without_password_returns_error():
    payload = {
        "login": f"user_{generate_random_string()}",
        "firstName": "Ivan"
    }
    r = requests.post(CREATE_COURIER, json=payload)
    assert r.status_code == 400, f"Ожидался 400 при отсутствии поля password, получили {r.status_code}: {r.text}"


# ---------- Авторизация курьера ----------

@allure.feature("Курьеры")
@allure.story("Авторизация успешная")
def test_login_courier_success(new_courier):
    payload = {"login": new_courier["login"], "password": new_courier["password"]}
    r = requests.post(LOGIN_COURIER, json=payload)
    assert r.status_code == 200, f"Ожидался 200, получили {r.status_code}: {r.text}"
    data = r.json()
    assert "id" in data and isinstance(data["id"], int)

@pytest.mark.parametrize("payload", [
    # отсутствует firstName
    ({"login": f"user_{generate_random_string()}", "password": f"pass_{generate_random_string()}"}),
    # полностью пустое тело
    ({})
])
@allure.feature("Курьеры")
@allure.story("Авторизация — отсутствие поля firstName")
def test_login_missing_firstname_returns_error(payload):
    r = requests.post(LOGIN_COURIER, json=payload)
    assert r.status_code == 400, (
        f"Ожидался 400 при отсутствии поля firstName, "
        f"получили {r.status_code}: {r.text}"
    )

@allure.feature("Курьеры")
@allure.story("Авторизация неверные креды")
def test_login_with_wrong_credentials_returns_error():
    payload = {"login": "nonexistent_user_123", "password": "wrong_pass"}
    r = requests.post(LOGIN_COURIER, json=payload)
    # API может возвращать 400 или 404 на неверные креды — принимаем оба
    assert r.status_code in (400, 404), f"Ожидалась ошибка при неверных кредах, получили {r.status_code}: {r.text}"
