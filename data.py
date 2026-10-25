
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
