import pytest
import requests
from create_new_courier import register_new_courier_and_return_login_password


url = 'https://qa-scooter.praktikum-services.ru'


@pytest.fixture
def create_courier():
    new_courier = register_new_courier_and_return_login_password()
    yield new_courier[0]
    new_courier_log_pass = {
        "login": new_courier[0][0],
        "password": new_courier[0][1]
    }
    response = requests.post(f'{url}/api/v1/courier/login', data=new_courier_log_pass)
    courier_id = response.json()['id']
    requests.delete(f'{url}/api/v1/courier/{courier_id}')

@pytest.fixture
def create_courier_response():
    new_courier = register_new_courier_and_return_login_password()
    yield new_courier[1]
    new_courier_log_pass = {
        "login": new_courier[0][0],
        "password": new_courier[0][1]
    }
    response = requests.post(f'{url}/api/v1/courier/login', data=new_courier_log_pass)
    courier_id = response.json()['id']
    requests.delete(f'{url}/api/v1/courier/{courier_id}')
