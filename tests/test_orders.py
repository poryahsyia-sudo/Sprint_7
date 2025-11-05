import pytest
import requests
import allure
from helpers.api_urls import CREATE_ORDER, GET_ORDERS
from data.orders_data import order_base


@allure.feature("Заказы")
class TestOrders:

    @pytest.mark.parametrize("color_option", [
        ["BLACK"], ["GREY"], ["BLACK", "GREY"], None
    ])
    @allure.story("Создание заказа с разными цветами")
    @allure.title("Создание заказа с цветом {color_option}")
    def test_create_order_with_different_colors(self, color_option):
        payload = dict(order_base)
        payload["color"] = color_option
        r = requests.post(CREATE_ORDER, json=payload)
        assert r.status_code == 201
        assert "track" in r.json()

    @allure.story("Получение списка заказов")
    @allure.title("Успешное получение списка заказов")
    def test_get_orders_list(self):
        r = requests.get(GET_ORDERS)
        assert r.status_code == 200
        assert "orders" in r.json()
