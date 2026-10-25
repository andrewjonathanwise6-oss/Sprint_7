
import allure
import pytest

from data import ORDER_DATA
from urls import ORDERS_URL


class TestCreateOrder:

    @allure.title('Создание заказа с разными цветами самоката')
    @pytest.mark.parametrize(
        'color',
        [
            ['BLACK'],
            ['GREY'],
            ['BLACK', 'GREY'],
            None
        ],
        ids=['black', 'grey', 'both_colors', 'without_color']
    )
    def test_create_order_returns_201_and_track(self, api_session, color):
        order_data = ORDER_DATA.copy()

        if color is not None:
            order_data['color'] = color

        response = api_session.post(
            ORDERS_URL,
            json=order_data,
            timeout=(30, 30)
        )

        assert response.status_code == 201
        assert isinstance(response.json().get('track'), int)
        assert response.json()['track'] > 0
