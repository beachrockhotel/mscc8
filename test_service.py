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

    # Тест взаимодействует как с веб-интерфейсом, так и с базой данных, что делает его интеграционным тестом для проверки функции добавления пункта меню
    def test_add_menu_item_service(self):
        with self.client:
            response = self.client.post('/menu', json={'name': 'Salad', 'price': 50})
            self.assertEqual(response.status_code, 201)
            self.assertIn('Позиция была создана', response.json['message'])


if __name__ == '__main__':
    unittest.main()
