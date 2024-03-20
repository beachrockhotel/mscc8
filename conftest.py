# conftest.py
import pytest
from unittest.mock import patch
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def authorized_client(client):
    with patch('auth.is_user_authenticated', return_value=True):
        yield client

def test_get_menu_authorized(authorized_client):
    response = authorized_client.get('/menu')
    assert response.status_code == 200
    # Дополнительно проверьте ожидаемый ответ

def test_add_menu_item_authorized(authorized_client):
    menu_item = {'name': 'New Dish', 'price': 12.50}
    response = authorized_client.post('/menu', json=menu_item)
    assert response.status_code == 201
    # Проверьте успешное добавление пункта меню

def test_make_order_authorized(authorized_client):
    order_data = {'item_ids': [1, 2, 3]}
    response = authorized_client.post('/order', json=order_data)
    assert response.status_code == 200
    # Проверьте создание заказа

def test_reserve_seat_authorized(authorized_client):
    reservation_data = {'user_name': 'testuser', 'seat_number': 1, 'time': '2023-01-01 12:00:00'}
    response = authorized_client.post('/reserve', json=reservation_data)
    assert response.status_code == 200
    # Проверьте успешное бронирование
