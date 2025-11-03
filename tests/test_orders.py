import pytest
import requests
import allure
from datetime import datetime, timedelta
from helpers.api_urls import CREATE_ORDER, GET_ORDERS

def make_order_payload(colors=None):
    delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    payload = {
        "firstName": "Ivan",
        "lastName": "Petrov",
        "address": "Москва, ул. Тестовая, д.1",
        "metroStation": "1",
        "phone": "+79991234567",
        "rentTime": 3,
        "deliveryDate": delivery_date,
        "comment": "Тестовый заказ"
    }
    if colors is not None:
        payload["color"] = colors
    return payload


@pytest.mark.parametrize("color_option", [
    (["BLACK"]),
    (["GREY"]),
    (["BLACK", "GREY"]),
    (None)
])
@allure.feature("Заказы")
@allure.story("Создание заказа с разными вариантами цвета")
def test_create_order_with_different_colors(color_option):
    with allure.step(f"Создание заказа с цветами: {color_option}"):
        payload = make_order_payload(colors=color_option)
        r = requests.post(CREATE_ORDER, json=payload)
        assert r.status_code == 201, f"Получен код {r.status_code}"
        data = r.json()
        assert "track" in data and isinstance(data["track"], int)


@allure.feature("Заказы")
@allure.story("Получение списка заказов")
def test_get_orders_list():
    r = requests.get(GET_ORDERS)
    assert r.status_code == 200
    data = r.json()
    assert "orders" in data and isinstance(data["orders"], list)
