import requests
import random
import string
from helpers.api_urls import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def register_courier():
    """Создаёт нового курьера и возвращает его данные"""
    login = f"user_{generate_random_string()}"
    password = f"pass_{generate_random_string()}"
    first_name = f"Name_{generate_random_string()}"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    r = requests.post(CREATE_COURIER, json=payload)
    r.raise_for_status()

    # Получаем id для удаления
    courier_id = get_courier_id(login, password)

    return {
        "id": courier_id,
        "login": login,
        "password": password
    }


def get_courier_id(login, password):
    r = requests.post(LOGIN_COURIER, json={"login": login, "password": password})
    if r.status_code == 200 and "id" in r.json():
        return r.json()["id"]
    return None


def delete_courier(courier_id):
    if courier_id:
        requests.delete(f"{DELETE_COURIER}/{courier_id}")
