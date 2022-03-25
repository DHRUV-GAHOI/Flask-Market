from flask_login import UserMixin
from market.app import db, login_manager, bcrypt
from user.models import *
from restaurant.models import *
from order.models import *
from dashboard.models import *
