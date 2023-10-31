import allure
import requests
from conftest import create_courier


class TestCreatingCourier:
    @allure.title('Проверка, что курьера можно создать')
    def test_courier_creation_successful(self):
        # создание курьера
        new_courier = {
            "login": "cat12",
            "password": "112233",
            "firstName": "cat12"
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/', data=new_courier)
        assert response.status_code == 201 and response.text == '{"ok":true}'
        # вход под курьером
        courier_log_pass = {
            "login": new_courier['login'],
            "password": new_courier['password']
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login/', data=courier_log_pass)
        courier_id = response.json()['id']
        assert response.status_code == 200
        # удаление курьера
        response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_cannot_create_two_identical_couriers(self, create_courier):
        new_courier = create_courier
        create_second_courier = {
            "login": new_courier[0],
            "password": new_courier[1],
            "firstName": new_courier[2]
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/', data=create_second_courier)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'
