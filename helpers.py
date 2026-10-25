import uuid


def generate_courier_data():
    unique_login = f'courier_{uuid.uuid4().hex[:12]}'

    return {
        'login': unique_login,
        'password': 'Password123',
        'firstName': 'TestCourier'
    }