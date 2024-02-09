import unittest
from app import app, db
from models import MenuItem

class ModelsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Устанавливаем конфигурацию тестовой базы данных один раз для всего класса
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dmitriy:321123@localhost/club_test'

    def setUp(self):
        # Создаем таблицы в контексте приложения
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Удаляем таблицы и очищаем сессию в контексте приложения
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_menu_item_model(self):
        # Работаем с базой данных в контексте приложения
        with app.app_context():
            # Очищаем таблицу MenuItem перед тестом
            db.session.query(MenuItem).delete()
            db.session.commit()

            # Добавляем новый элемент в базу данных
            item = MenuItem(name="Test Pizza", price=100.0)
            db.session.add(item)
            db.session.commit()

            # Проверяем, что в таблице ровно один элемент
            self.assertEqual(MenuItem.query.count(), 1)
