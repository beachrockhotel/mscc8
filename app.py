from flask import Flask
from flask import request, render_template
from models import db
from prometheus_flask_exporter import PrometheusMetrics
import os
from menu_service import add_menu_item, get_menu, make_order, get_orders
from reservation_service import reserve_seat, get_reservations, check_availability, cancel_reservation

app = Flask(__name__)

metrics = PrometheusMetrics(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://dmitriy:321123@localhost/club')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

is_db_initialized = False

@app.before_request
def create_tables():
    global is_db_initialized
    if not is_db_initialized:
        db.create_all()
        is_db_initialized = True

@app.route('/')
def home():
        return render_template('index.html')

@app.route('/menu', methods=['POST'])
def add_menu_endpoint():
    return add_menu_item()

@app.route('/menu', methods=['GET'])
def get_menu_endpoint():
        return get_menu()

@app.route('/order', methods=['POST'])
def order_endpoint():
    return make_order()

@app.route('/orders', methods=['GET'])
def orders_endpoint():
        return get_orders()

@app.route('/reserve', methods=['POST'])
def reserve():
    return reserve_seat()

@app.route('/reservations', methods=['GET'])
def reservations():
        return get_reservations()

@app.route('/check_availability', methods=['POST'])
def availability():
    return check_availability()

@app.route('/cancel_reservation/<int:reservation_id>', methods=['DELETE'])
def cancel(reservation_id):
    return cancel_reservation(reservation_id)


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5002'))
    app.run(debug=True, port=port)