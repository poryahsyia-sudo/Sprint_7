import pytest
from helpers.register_new_courier import register_courier, delete_courier


@pytest.fixture
def new_courier():
    """Создаёт курьера перед тестом и удаляет после"""
    courier = register_courier()
    yield courier
    delete_courier(courier["id"])
