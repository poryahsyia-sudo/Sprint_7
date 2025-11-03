import pytest
import requests
import allure
from helpers.api_urls import CREATE_ORDER, GET_ORDERS


@allure.feature("Заказы")
class TestOrders:

    @pytest.mark.parametrize("color_option", [
        ["BLACK"], ["GREY"], ["BLACK", "GREY"], None
    ])
    @allure.story("Создание заказа с разными цветами")
    def test_create_order_with_different_colors(self, color_option):
        payload = {
            "firstName": "Ivan",
            "lastName": "Petrov",
            "address": "Moscow",
            "metroStation": 4,
            "phone": "+79998887766",
            "rentTime": 5,
            "deliveryDate": "2025-12-01",
            "comment": "Test order",
            "color": color_option
        }
        r = requests.post(CREATE_ORDER, json=payload)
        assert r.status_code == 201
        assert "track" in r.json()

    @allure.story("Получение списка заказов")
    def test_get_orders_list(self):
        r = requests.get(GET_ORDERS)
        assert r.status_code == 200
        assert "orders" in r.json()
