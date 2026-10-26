
import allure
import pytest

from helpers import generate_courier_data
from urls import COURIER_LOGIN_URL
from data import LOGIN_MISSING_DATA_MESSAGE, LOGIN_NOT_FOUND_MESSAGE


class TestLoginCourier:

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_returns_200_and_id(
            self, api_session, registered_courier
    ):
        response = api_session.post(
            COURIER_LOGIN_URL,
            json={
                'login': registered_courier['login'],
                'password': registered_courier['password']
            },
            timeout=(30, 30)
        )

        assert response.status_code == 200
        assert isinstance(response.json().get('id'), int)

    @allure.title('Авторизация без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_without_required_field_returns_400(
            self, api_session, registered_courier, missing_field
    ):
        login_data = {
            'login': registered_courier['login'],
            'password': registered_courier['password']
        }

        del login_data[missing_field]

        response = api_session.post(
            COURIER_LOGIN_URL,
            json=login_data,
            timeout=(30, 30)
        )

        assert response.status_code == 400
        assert response.json()['message'] == LOGIN_MISSING_DATA_MESSAGE, response.text

    @allure.title('Авторизация с неверным полем: {wrong_field}')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_with_wrong_credentials_returns_404(
            self, api_session, registered_courier, wrong_field
    ):
        login_data = {
            'login': registered_courier['login'],
            'password': registered_courier['password']
        }

        login_data[wrong_field] += '_wrong'

        response = api_session.post(
            COURIER_LOGIN_URL,
            json=login_data,
            timeout=(30, 30)
        )

        assert response.status_code == 404
        assert response.json()['message'] == LOGIN_NOT_FOUND_MESSAGE, response.text

    @allure.title('Авторизация несуществующего курьера')
    def test_login_nonexistent_courier_returns_404(self, api_session):
        courier_data = generate_courier_data()

        response = api_session.post(
            COURIER_LOGIN_URL,
            json={
                'login': courier_data['login'],
                'password': courier_data['password']
            },
            timeout=(30, 30)
        )

        assert response.status_code == 404
        assert response.json()['message'] == LOGIN_NOT_FOUND_MESSAGE, response.text
