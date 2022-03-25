# Dashboard models
from market.app import db

class Dashboard(db.Model):
    __tablename__ = 'dashboard'
    id = db.Column(db.Integer(), primary_key=True)
    
    user_success=db.Column(db.Integer(),default=0)
    user_fail=db.Column(db.Integer(),default=0)
    
    order_success=db.Column(db.Integer(),default=0)
    order_fail=db.Column(db.Integer(),default=0)
    
    item_success=db.Column(db.Integer(),default=0)
    item_fail=db.Column(db.Integer(),default=0)
    
    hotel_success=db.Column(db.Integer(),default=0)
    hotel_fail=db.Column(db.Integer(),default=0)
    