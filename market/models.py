from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
from market import db, login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    orders = db.relationship('Order', backref='user', lazy=True)
    

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    orders = db.relationship('Order', backref='hotel', lazy=True)
    location= db.Column(db.String(length=1024), nullable=False, unique=True)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    # orders=db.relationship('Order',secondary='item_order',backref=db.backref('items',lazy=True))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
  
    def __repr__(self):
        return f'Item {self.name}'


# item_order_assosiation=db.Table('item_order',
#                                 db.Column('item_id',db.Integer,db.ForeignKey('item.id')),
#                                 db.Column('order_id',db.Integer,db.ForeignKey('order.id')))
# #order.items.append()

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True)
    # uni_id=db.Column(db.())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    cost=db.Column(db.Integer(),default=0)
    items = db.relationship('Item', backref='order', lazy=True)
    order_completed = db.Column(db.Boolean(), default=False)