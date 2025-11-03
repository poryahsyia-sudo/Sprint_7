import requests
import random
import string
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

def generate_random_string(length=8):
    """Создаёт случайную строку из букв и цифр."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает [login, password, firstName].
    Если регистрация не удалась — возвращает пустой список.
    """
    login = f"user_{generate_random_string()}"
    password = f"pass_{generate_random_string()}"
    first_name = f"name_{generate_random_string(5)}"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(CREATE_COURIER, json=payload)

    # возвращаем данные при успешной регистрации (201)
    if response.status_code == 201:
        return [login, password, first_name]

    # иначе печатаем (чтобы в логах было видно) и возвращаем пустой список
    print(f"Register courier failed: {response.status_code} | {response.text}")
    return []

def login_and_get_id(login, password):
    """
    Авторизация курьера — возвращает id (int) при успехе, иначе None.
    """
    payload = {"login": login, "password": password}
    response = requests.post(LOGIN_COURIER, json=payload)
    if response.status_code == 200:
        try:
            return response.json().get("id")
        except ValueError:
            return None
    return None

def delete_courier_by_id(courier_id):
    """
    Удаляет курьера по id. Возвращает True если удаление успешно (200), иначе False.
    """
    response = requests.delete(f"{DELETE_COURIER}/{courier_id}")
    return response.status_code == 200
