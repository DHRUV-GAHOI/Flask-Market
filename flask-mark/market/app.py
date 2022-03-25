from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes
from user.user import user_bp
from order.order import order_bp
from restaurant.restaurant import restaurant_bp
from dashboard.dashboard import dashboard_bp

app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(restaurant_bp)
app.register_blueprint(dashboard_bp)
