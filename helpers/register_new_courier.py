import requests
import random
import string
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает [login, password, firstName]
    Если регистрация не удалась — возвращает пустой список.
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(CREATE_COURIER, json=payload)
    if response.status_code == 201:
        return [login, password, first_name]
    return []

def login_and_get_id(login, password):
    """Авторизация курьера — возвращает id при успехе, иначе None."""
    payload = {"login": login, "password": password}
    response = requests.post(LOGIN_COURIER, json=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def delete_courier_by_id(courier_id):
    """Удаляет курьера по id. Возвращает True при успехе."""
    response = requests.delete(f"{DELETE_COURIER}/{courier_id}")
    return response.status_code == 200
