import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'https://petstore.swagger.rv-school.ru/api/v3'


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 99999,
                "name": "Non-existent Pet",
                "status": "available"
            }

        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Отправка запроса на добавление нового питомца"):
            payload = {
                      "id"       : 1,
                      "name"     : "Buddy",
                      "status"   : "available"
            }



        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload )
            response_json = response.json()

        with allure.step("Проверка статуса ответа и JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"



    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_with_full_info(self):
        with allure.step("Отправка запроса на добавление нового питомца c полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }


        with allure.step("Отправка запроса на создание питомца c полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе c полными данными"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "category питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "tags питомца не совпадает с ожидаемым"

