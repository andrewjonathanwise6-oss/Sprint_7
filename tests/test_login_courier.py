
import allure
import pytest

from helpers import generate_courier_data
from urls import COURIER_URL, COURIER_LOGIN_URL


class TestLoginCourier:

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_returns_200_and_id(self, api_session, courier_cleanup):
        courier_data = generate_courier_data()

        create_response = api_session.post(
            COURIER_URL,
            json=courier_data,
            timeout=(30, 30)
        )

        assert create_response.status_code == 201
        courier_cleanup.append(courier_data)

        login_response = api_session.post(
            COURIER_LOGIN_URL,
            json={
                'login': courier_data['login'],
                'password': courier_data['password']
            },
            timeout=(30, 30)
        )

        assert login_response.status_code == 200
        assert isinstance(login_response.json().get('id'), int)

    @allure.title('Авторизация без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_without_required_field_returns_400(
            self, api_session, courier_cleanup, missing_field
    ):
        courier_data = generate_courier_data()

        if missing_field == 'password':
            create_response = api_session.post(
                COURIER_URL,
                json=courier_data,
                timeout=(30, 30)
            )

            assert create_response.status_code == 201
            courier_cleanup.append(courier_data)

        login_data = {
            'login': courier_data['login'],
            'password': courier_data['password']
        }

        del login_data[missing_field]

        response = api_session.post(
            COURIER_LOGIN_URL,
            json=login_data,
            timeout=(30, 75)
        )

        assert response.status_code == 400, (
            f'Получен статус {response.status_code}: {response.text[:300]}'
        )
        assert 'message' in response.json()

    @allure.title('Авторизация с неверным полем: {wrong_field}')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_with_wrong_credentials_returns_404(
            self, api_session, courier_cleanup, wrong_field
    ):
        courier_data = generate_courier_data()

        create_response = api_session.post(
            COURIER_URL,
            json=courier_data,
            timeout=(30, 30)
        )

        assert create_response.status_code == 201
        courier_cleanup.append(courier_data)

        login_data = {
            'login': courier_data['login'],
            'password': courier_data['password']
        }

        login_data[wrong_field] += '_wrong'

        response = api_session.post(
            COURIER_LOGIN_URL,
            json=login_data,
            timeout=(30, 30)
        )

        assert response.status_code == 404
        assert 'message' in response.json()

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
        assert 'message' in response.json()
