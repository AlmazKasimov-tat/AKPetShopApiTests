import allure
import requests
import pytest


BASE_URL = 'https://petstore.swagger.rv-school.ru/api/v3'


@allure.feature("store")
class TestStoreAuto:
    @allure.title('Попытка разместить заказ')
    def test_order_placement(self):
        with allure.step("Отправка запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса кода ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json['status'] == payload['status'], "status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete заказа не совпадает с ожидаемым"


    @allure.title("Попытка получить информацию о заказе по ID")
    def test_order_info_by_id(self):
        with allure.step("Отправка запроса о получении информации по заказу (по ID)"):
            payload = {
                "id": 1
            }
            response = requests.get(url=f"{BASE_URL}/store/order/{payload['id']}")
            response_json = response.json()

        with allure.step("Проверка полученного статуса и совпадение по ID"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"


    @allure.title("Попытка удалить заказ по ID")
    def test_delete_order_by_id(self):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            payload = {
                "id": 1
            }
            response = requests.delete(url=f"{BASE_URL}/store/order/{payload['id']}")
            response_json = response.json()

        with allure.step("Проверка статуса успешного удаления по ID"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"


        with allure.step("Отправка запроса GET на проверку, что удаленного заказа не существует"):
            response = requests.get(url=f"{BASE_URL}/store/order/{payload['id']}")


        with allure.step("Проверка, что запрашиваемый заказ не найден"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
            assert response.text == "Order not found", "Код ответа не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_info_about_non_existent_order(self):
        with allure.step("Отправка запроса на проверку инфо о заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса успешного удаления по ID"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
            assert response.text == "Order not found", "Код ответа не совпал с ожидаемым"


    @allure.title("Попытка получения инвентаря магазина")
    def test_get_info_about_inventory(self):
        """
           Получение инвентаря магазина (GET /store/inventory)
           """
        with allure.step("Отправить GET-запрос на /store/inventory"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

            # Проверяем, что ответ валидный JSON
            response_json = response.json()
            assert isinstance(response_json, dict), "Ответ должен быть JSON объектом (словарем)"

            # Проверяем, что ответ содержит данные инвентаря (статусы в виде ключей, количества в виде значений)
            # Пример ответа: {"approved": 57, "delivered": 50, "placed": 100}
            assert len(response_json) > 0, "Инвентарь не должен быть пустым"

            # Проверяем, что все ключи - строки (статусы), а значения - числа (количества)
            for status, count in response_json.items():
                assert isinstance(status, str), f"Ключ '{status}' должен быть строкой (статус заказа)"
                assert isinstance(count, int), f"Значение для статуса '{status}' должно быть числом"
                assert count >= 0, f"Количество для статуса '{status}' не может быть отрицательным"


