import pytest
import requests
import allure
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER
from helpers.register_new_courier import generate_random_string, register_courier, delete_courier


@allure.feature("Курьеры")
class TestCreateCourier:

    @allure.story("Создание курьера — успешное")
    def test_create_courier_success(self):
        payload = {
            "login": f"user_{generate_random_string()}",
            "password": f"pass_{generate_random_string()}",
            "firstName": "Ivan"
        }
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 201
        assert r.json().get("ok") is True

        # cleanup
        courier_id = requests.post(LOGIN_COURIER, json={
            "login": payload["login"], "password": payload["password"]
        }).json().get("id")
        delete_courier(courier_id)

    @allure.story("Создание курьера — дубликат")
    def test_create_duplicate_courier_fails(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": "Ivan"
        }
        r = requests.post(CREATE_COURIER, json=payload)
        assert r.status_code == 409
        assert "message" in r.json()


    @pytest.mark.parametrize("missing_field,payload", [
        ("login", {"password": "pass", "firstName": "Ivan"}),
        # чтобы избежать 409, генерируем уникальные данные
        ("password", {"login": f"user_{generate_random_string()}", "firstName": "Ivan"}),
        ("firstName", {"login": f"user_{generate_random_string()}", "password": "pass"})
    ])
    @allure.story("Создание курьера — отсутствует обязательное поле")
    def test_create_courier_missing_field_returns_error(self, missing_field, payload):
        r = requests.post(CREATE_COURIER, json=payload)
        if missing_field == "firstName":
            # firstName не обязательное поле, ожидаем 201
            assert r.status_code == 201, (
                f"Ожидался 201 при отсутствии поля {missing_field}, получили {r.status_code}: {r.text}"
            )
            assert r.json().get("ok") is True
            courier_id = requests.post(LOGIN_COURIER, json={
                "login": payload["login"], "password": payload["password"]
            }).json().get("id")
            delete_courier(courier_id)
        else:
            # login и password обязательны
            assert r.status_code == 400, (
                f"Ожидался 400 при отсутствии поля {missing_field}, получили {r.status_code}: {r.text}"
            )
            assert "message" in r.json()


@allure.feature("Курьеры")
class TestLoginCourier:

    @allure.story("Авторизация курьера — успешная")
    def test_login_courier_success(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"]
        }
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 200
        assert "id" in r.json()

    @allure.story("Авторизация — неверные данные")
    def test_login_with_wrong_credentials_returns_error(self):
        payload = {"login": "wrong_user", "password": "wrong_pass"}
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 404
        assert "message" in r.json()

    @pytest.mark.parametrize("payload", [
        ({"firstName": "Ivan"}),  # вместо логина пропускаем login
        ({"firstName": "Ivan", "password": "1234"}),
        ({})
    ])
    @allure.story("Авторизация — отсутствуют обязательные поля")
    def test_login_missing_fields_returns_error(self, payload):
        r = requests.post(LOGIN_COURIER, json=payload)
        assert r.status_code == 400, (
            f"Ожидался 400 при отсутствии обязательных полей, получили {r.status_code}: {r.text}"
        )
        assert "message" in r.json()
