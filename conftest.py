import pytest
import requests
from create_new_courier import register_new_courier_and_return_login_password


@pytest.fixture
def create_courier():
    new_courier = register_new_courier_and_return_login_password()
    yield new_courier
    new_courier_log_pass = {
        "login": new_courier[0],
        "password": new_courier[1]
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=new_courier_log_pass)
    courier_id = response.json()['id']
    # удаление курьера
    requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
