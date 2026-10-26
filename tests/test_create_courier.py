
import allure
import pytest

from helpers import generate_courier_data
from urls import COURIER_URL
from data import (
    COURIER_ALREADY_EXISTS_MESSAGE,
    COURIER_MISSING_DATA_MESSAGE
)


class TestCreateCourier:

    @allure.title('Успешное создание курьера')
    def test_create_courier_returns_201_and_ok_true(
            self, api_session, courier_cleanup
    ):
        courier_data = generate_courier_data()

        response = api_session.post(
            COURIER_URL,
            json=courier_data,
            timeout=(30, 30)
        )

        courier_cleanup.append(courier_data)

        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Нельзя создать двух курьеров с одинаковым логином')
    def test_create_duplicate_courier_returns_409(
            self, api_session, courier_cleanup
    ):
        courier_data = generate_courier_data()

        api_session.post(
            COURIER_URL,
            json=courier_data,
            timeout=(30, 30)
        )

        courier_cleanup.append(courier_data)

        response = api_session.post(
            COURIER_URL,
            json=courier_data,
            timeout=(30, 30)
        )

        assert response.status_code == 409
        assert response.json()['message'] == COURIER_ALREADY_EXISTS_MESSAGE, response.text

    @allure.title('Создание курьера без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_without_required_field_returns_400(
            self, api_session, missing_field
    ):
        courier_data = generate_courier_data()
        del courier_data[missing_field]

        response = api_session.post(
            COURIER_URL,
            json=courier_data,
            timeout=(30, 30)
        )

        assert response.status_code == 400
        assert response.json()['message'] == COURIER_MISSING_DATA_MESSAGE
