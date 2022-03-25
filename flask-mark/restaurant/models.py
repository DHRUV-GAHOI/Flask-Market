# Restaurant models
from market.app import db

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

