# Order Models
from market.app import db

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True)
    # uni_id=db.Column(db.())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    cost=db.Column(db.Integer(),default=0)
    items = db.relationship('Item', backref='order', lazy=True)
    order_completed = db.Column(db.Boolean(), default=False)
    
    
class OrderItemCount(db.Model):
    __tablename__ = 'orderitemcount'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item_count = db.Column(db.Integer, default=0)