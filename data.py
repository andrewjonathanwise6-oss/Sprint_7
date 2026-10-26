
from datetime import date, timedelta


ORDER_DATA = {
    'firstName': 'Test',
    'lastName': 'User',
    'address': 'Moscow, Test street, 10',
    'metroStation': 4,
    'phone': '+79991234567',
    'rentTime': 2,
    'deliveryDate': (date.today() + timedelta(days=3)).isoformat(),
    'comment': 'API automated test'
}

COURIER_ALREADY_EXISTS_MESSAGE = 'Этот логин уже используется. Попробуйте другой.'
COURIER_MISSING_DATA_MESSAGE = 'Недостаточно данных для создания учетной записи'
LOGIN_MISSING_DATA_MESSAGE = 'Недостаточно данных для входа'
LOGIN_NOT_FOUND_MESSAGE = 'Учетная запись не найдена'