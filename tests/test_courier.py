import pytest
import requests
import allure
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER
from helpers.register_new_courier import generate_random_string


@allure.feature("Курьеры")
class TestCreateCourier:

    @allure.story("Создание курьера — успешное")
    @allure.title("Успешное создание нового курьера")
    def test_create_courier_success(self):
        payload = {
            "login": f"user_{generate_random_string()}",
            "password": f"pass_{generate_random_string()}",
            "firstName": "Ivan"
        }
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 201
        assert r.json().get("ok") is True

    @allure.story("Создание курьера — дубликат")
    @allure.title("Попытка создать курьера с существующими данными вызывает ошибку 409")
    def test_create_duplicate_courier_fails(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": "Ivan"
        }
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 409
        assert "message" in r.json()

    @allure.story("Создание курьера — отсутствует обязательное поле 'login'")
    @allure.title("Ошибка при отсутствии поля 'login'")
    def test_create_courier_without_login_returns_error(self):
        payload = {"password": "pass", "firstName": "Ivan"}
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 400
        assert "message" in r.json()

    @allure.story("Создание курьера — отсутствует обязательное поле 'password'")
    @allure.title("Ошибка при отсутствии поля 'password'")
    def test_create_courier_without_password_returns_error(self):
        payload = {"login": f"user_{generate_random_string()}", "firstName": "Ivan"}
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 400
        assert "message" in r.json()

    @allure.story("Создание курьера — необязательное поле 'firstName'")
    @allure.title("Курьер успешно создаётся без поля 'firstName'")
    def test_create_courier_without_first_name_success(self):
        payload = {"login": f"user_{generate_random_string()}", "password": "pass"}
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 201
        assert r.json().get("ok") is True


@allure.feature("Курьеры")
class TestLoginCourier:

    @allure.story("Авторизация курьера — успешная")
    @allure.title("Успешный вход курьера в систему")
    def test_login_courier_success(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"]
        }
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 200
        assert "id" in r.json()

    @allure.story("Авторизация — неверные данные")
    @allure.title("Ошибка при вводе неверных логина и пароля")
    def test_login_with_wrong_credentials_returns_error(self):
        payload = {"login": "wrong_user", "password": "wrong_pass"}
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 404
        assert "message" in r.json()

    @allure.story("Авторизация — отсутствует обязательное поле 'login'")
    @allure.title("Ошибка при отсутствии поля 'login'")
    def test_login_without_login_returns_error(self):
        payload = {"password": "1234"}
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 400
        assert "message" in r.json()

    @allure.story("Авторизация — отсутствует обязательное поле 'password'")
    @allure.title("Ошибка при отсутствии поля 'password'")
    def test_login_without_password_returns_error(self):
        payload = {"login": "user_test"}
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 400
        assert "message" in r.json()

    @allure.story("Авторизация — отсутствуют оба обязательных поля")
    @allure.title("Ошибка при отсутствии логина и пароля")
    def test_login_without_fields_returns_error(self):
        r = requests.post(LOGIN_COURIER, json={})
        assert r.status_code == 400
        assert "message" in r.json()
