import json
import allure
import pytest
import requests
from conftest import create_courier


url = 'https://qa-scooter.praktikum-services.ru'


class TestCreatingCourier:
    @allure.title('Проверка, что курьера можно создать')
    def test_courier_creation_successful(self, create_courier_response):
        new_courier = create_courier_response
        assert new_courier.status_code == 201 and new_courier.text == '{"ok":true}'

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_cannot_create_two_identical_couriers(self, create_courier):
        new_courier = create_courier
        create_second_courier = {
            "login": new_courier[0],
            "password": new_courier[1],
            "firstName": new_courier[2]
        }
        response = requests.post(f'{url}/api/v1/courier/',
                                 data=create_second_courier)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'

    @allure.title('Создание курьера без заполнения обязательного поля логина или пароля')
    @pytest.mark.parametrize('login, password, first_name', [['cat91', '', 'cat91'], ['', '112233', 'cat92']])
    def test_create_courier_without_login_or_password(self, login, password, first_name):
        courier_without_log_or_pass = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{url}/api/v1/courier/',
                                 data=courier_without_log_or_pass)
        assert (response.status_code == 400 and
                response.text == '{"message": "Недостаточно данных для создания учетной записи"}')

    @allure.title('Создание курьеров с одинаковыми логинами')
    def test_cannot_create_couriers_with_the_same_logins(self, create_courier):
        new_courier = create_courier
        create_second_courier = {
            "login": new_courier[0],
            "password": "123123",
            "firstName": "Roma"
        }
        response = requests.post(f'{url}/api/v1/courier/',
                                 data=create_second_courier)
        assert response.status_code == 409 and response.text == '{"message": "Этот логин уже используется"}'


class TestLoginCourier:
    @allure.title('Успешная авторизация курьера в системе')
    def test_successful_courier_authorization(self, create_courier):
        new_courier = create_courier
        courier_log_pass = {
            "login": new_courier[0],
            "password": new_courier[1]
        }
        response = requests.post(f'{url}/api/v1/courier/login/', data=courier_log_pass)
        courier_id = response.json()['id']
        assert response.status_code == 200 and response.text == f'{{id: {courier_id}}}'

    @allure.title('Авторизация курьера с неверным логином')
    def test_authorization_with_incorrect_login(self, create_courier):
        new_courier = create_courier
        courier_with_incorrect_log = {
            "login": "caaat",
            "password": new_courier[1],
            "firstName": new_courier[2]
        }
        response = requests.post(f'{url}/api/v1/courier/login',
                                 data=courier_with_incorrect_log)
        assert response.status_code == 404 and response.text == {"message": "Учетная запись не найдена"}

    @allure.title('Авторизация курьера с неверным паролем')
    def test_authorization_with_incorrect_password(self, create_courier):
        new_courier = create_courier
        courier_with_incorrect_pass = {
            "login": new_courier[0],
            "password": "112233",
            "firstName": new_courier[2]
        }
        response = requests.post(f'{url}/api/v1/courier/login',
                                 data=courier_with_incorrect_pass)
        assert response.status_code == 404 and response.text == {"message": "Учетная запись не найдена"}

    @allure.title('Авторизация курьера без логина')
    def test_authorization_without_login(self, create_courier):
        new_courier = create_courier
        courier_without_log = {
            "login": "",
            "password": new_courier[1],
            "firstName": new_courier[2]
        }
        response = requests.post(f'{url}/api/v1/courier/login',
                                 data=courier_without_log)
        assert response.status_code == 400 and response.text == {"message":  "Недостаточно данных для входа"}

    @allure.title('Авторизация курьера без пароля')
    def test_authorization_without_password(self, create_courier):
        new_courier = create_courier
        courier_without_pass = {
            "login": new_courier[0],
            "password": "",
            "firstName": new_courier[2]
        }
        response = requests.post(f'{url}/api/v1/courier/login',
                                 data=courier_without_pass)
        assert response.status_code == 400 and response.text == {"message":  "Недостаточно данных для входа"}


class TestCreatingOrder:
    @allure.title('Выбор цвета самоката при создании заказа')
    @pytest.mark.parametrize('color', ['BLACK', 'GRAY', ['BLACK', 'GRAY'], ''])
    def test_choosing_the_color_of_the_scooter_when_creating_order(self, color):
        create_order = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": [color]
        }
        create_order_string = json.dumps(create_order)
        response = requests.post(f'{url}/api/v1/orders', data=create_order_string)
        track_id = response.json()['track']
        assert response.status_code == 201 and response.text == f'{{track: {track_id}}}'


class TestOrderList:
    @allure.title('Получение списка заказов без courierId')
    def test_get_list_of_order_without_courier_id(self):
        response = requests.get(f'{url}/api/v1/orders')
        assert response.status_code == 200 and len(response.text) > 0
