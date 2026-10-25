
import allure

from urls import ORDERS_URL


class TestGetOrders:

    @allure.title('Получение списка заказов')
    def test_get_orders_returns_200_and_orders_list(self, api_session):
        response = api_session.get(
            ORDERS_URL,
            timeout=(30, 60)
        )

        assert response.status_code == 200

        response_data = response.json()

        assert 'orders' in response_data
        assert isinstance(response_data['orders'], list)
