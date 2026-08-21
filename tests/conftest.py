import pytest
import requests

BASE_URL = 'https://petstore.swagger.rv-school.ru/api/v3'

@pytest.fixture(scope='function')
def create_pet():
    """Фикстура для создания питомца."""
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }


    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope="function")
def existing_order():
    create_payload = {
        "petId": 12345,
        "quantity": 1,
        "shipDate": "2026-08-21T12:00:00.000Z",
        "status": "placed",
        "complete": False
    }

    create_response = requests.post(f"{BASE_URL}/store/order", json=create_payload)
    assert create_response.status_code == 200, f"Не удалось создать заказ для теста. Ответ: {create_response.text}"

    order_data = create_response.json()

    yield order_data

    requests.delete(f"{BASE_URL}/store/order/{order_data['id']}")