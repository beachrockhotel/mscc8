# tests/test_services.py
import unittest
from flask_testing import TestCase
from app import app, db
from models import MenuItem, Reservation

class ServicesTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dmitriy:321123@localhost/club_test'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_menu_item_service(self):
        with self.client:
            response = self.client.post('/menu', json={'name': 'Salad', 'price': 50})
            self.assertEqual(response.status_code, 201)
            self.assertIn('Позиция была создана', response.json['message'])

    def test_get_menu_service(self):
        # Добавим предварительно элемент меню для теста
        with self.client:
            self.client.post('/menu', json={'name': 'Soup', 'price': 30})
            # Теперь проверяем, что мы можем получить список меню через GET запрос
            response = self.client.get('/menu')
            self.assertEqual(response.status_code, 200)
            # Убедимся, что в ответе есть добавленный элемент
            self.assertIn('Soup', response.json['menu'][0]['name'])
            self.assertEqual(response.json['menu'][0]['price'], 30)

    def test_make_order(self):
        # Сначала добавляем элемент в меню, чтобы было что заказывать
        with self.client:
            add_response = self.client.post('/menu', json={'name': 'Sandwich', 'price': 50})
            menu_item_id = add_response.json['id']
            # Теперь создаем заказ с этим элементом
            order_response = self.client.post('/order', json={'item_ids': [menu_item_id]})
            self.assertEqual(order_response.status_code, 200)
            self.assertIn('Sandwich', order_response.json['items'])

    def test_reserve_seat(self):
        # Создаем бронирование места
        with self.client:
            response = self.client.post('/reserve', json={
                'user_name': 'Demon Komarov',
                'seat_number': 12,
                'time': '2024-03-21 19:00:00'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('Место успешно забронировано', response.json['message'])


if __name__ == '__main__':
    unittest.main()
