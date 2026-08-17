import allure
import requests
import jsonschema
import pytest
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


    @allure.title("Получение информации о питомце по ID")
    def test_add_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id


    @allure.title("Обновление информации о питомце по ID")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]


        payload = {
            "id": pet_id,
            "name": "Buddy Updated",
            "status": "sold",
            "photoUrls": [],
            "tags": []
        }

        with allure.step("Отправка запроса на обновление информации о питомце"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, f"Ошибка обновления: {response.text}"

            updated_pet = response.json()
            assert updated_pet["id"] == pet_id
            assert updated_pet["name"] == "Buddy Updated"
            assert updated_pet["status"] == "sold"


    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            delete_response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert delete_response.status_code == 200, f"Ошибка удаления: {delete_response.text}"

        with allure.step("Проверка, что питомец действительно удален"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, "Питомец не был удален!"


    @allure.title("Получение питомца по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("sold", 200),
            ("borrowed", 200),
            ("", 200)
        ],
    )
    def test_get_pet_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомца по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code, f"Ошибка удаления: {response.text}"
            assert isinstance(response.json(), list)


