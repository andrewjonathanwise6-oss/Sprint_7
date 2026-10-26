import pytest
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from helpers import generate_courier_data

from urls import COURIER_URL, COURIER_LOGIN_URL


@pytest.fixture
def api_session():
    retry_strategy = Retry(
        total=3,
        connect=3,
        read=0,
        status=0,
        backoff_factor=1
    )

    with requests.Session() as session:
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('https://', adapter)
        yield session


@pytest.fixture
def courier_cleanup(api_session):
    created_couriers = []

    yield created_couriers

    for courier in created_couriers:
        login_response = api_session.post(
            COURIER_LOGIN_URL,
            json={
                'login': courier['login'],
                'password': courier['password']
            },
            timeout=(30, 30)
        )

        assert login_response.status_code == 200

        courier_id = login_response.json()['id']

        delete_response = api_session.delete(
            f'{COURIER_URL}/{courier_id}',
            timeout=(30, 30)
        )

        assert delete_response.status_code == 200
        assert delete_response.json() == {'ok': True}

@pytest.fixture
def registered_courier(api_session, courier_cleanup):
    courier_data = generate_courier_data()

    response = api_session.post(
        COURIER_URL,
        json=courier_data,
        timeout=(30, 30)
    )

    response.raise_for_status()
    courier_cleanup.append(courier_data)

    return courier_data