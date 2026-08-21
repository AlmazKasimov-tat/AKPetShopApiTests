import allure
import requests
import pytest
import jsonschema


from .schemas.store_shema import STORE_SCHEMA, INVENTORY_SCHEMA

BASE_URL = 'https://petstore.swagger.rv-school.ru/api/v3'



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



@allure.feature("Store")
class TestStoreAuto:

    @allure.title('Попытка разместить заказ')
    def test_order_placement(self):
        with allure.step("Отправка запроса на размещение заказа"):
            payload = {
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса кода ответа и схемы"):
            assert response.status_code == 200, f"Код ответа не совпал с ожидаемым. Текст: {response.text}"
            jsonschema.validate(response_json, STORE_SCHEMA)

    @allure.title("Попытка получить информацию о заказе по ID")
    def test_get_order_info_by_id(self, existing_order):
        real_order_id = existing_order["id"]

        with allure.step(f"Отправка запроса о получении информации по заказу ID: {real_order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{real_order_id}")
            response_json = response.json()

        with allure.step("Проверка полученного статуса и совпадение по ID"):
            assert response.status_code == 200, f"Код ответа не совпал с ожидаемым. Текст: {response.text}"
            assert response_json["id"] == real_order_id, "ID в ответе не совпадает с запрошенным"
            jsonschema.validate(response_json, STORE_SCHEMA)

    @allure.title("Попытка удалить заказ по ID")
    def test_delete_order_by_id(self, existing_order):
        real_order_id = existing_order["id"]

        with allure.step(f"Отправка запроса на удаление заказа по ID: {real_order_id}"):
            delete_response = requests.delete(url=f"{BASE_URL}/store/order/{real_order_id}")

        with allure.step("Проверка статуса успешного удаления"):
            assert delete_response.status_code in (200, 204), \
                f"Ожидался 200 или 204, получен {delete_response.status_code}"

        with allure.step("Проверка, что запрашиваемый заказ больше не найден"):
            get_response = requests.get(url=f"{BASE_URL}/store/order/{real_order_id}")

            assert get_response.status_code == 404, \
                f"Ожидался 404, получен {get_response.status_code}"

            # ИСПРАВЛЕНО: используем response.text вместо response.json()
            assert "not found" in get_response.text.lower(), \
                f"Сообщение об ошибке не содержит 'not found'. Получено: {get_response.text}"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_info_about_non_existent_order(self):
        fake_order_id = 999999999

        with allure.step(f"Отправка запроса на проверку инфо о несуществующем заказе {fake_order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{fake_order_id}")

        with allure.step("Проверка, что возвращается 404"):
            assert response.status_code == 404, \
                f"Код ответа не совпал с ожидаемым. Текст: {response.text}"

            assert "not found" in response.text.lower(), \
                f"Сообщение об ошибке некорректно. Получено: {response.text}"


    @allure.title("Попытка получения инвентаря магазина")
    def test_get_info_about_inventory(self):
        with allure.step("Отправить GET-запрос на /store/inventory"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и формата данных по JSON Schema"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

            jsonschema.validate(instance=response_json, schema=INVENTORY_SCHEMA)