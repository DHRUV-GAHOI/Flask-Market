from market.app import db, app
from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.models import *
from market.forms import RegisterForm, LoginForm, Itemform, HotelForm
import json
from flask_login import login_user, logout_user, login_required, current_user

order_bp = Blueprint('order_bp', __name__, template_folder='templates')


@order_bp.route('/buy_page/<id>')
@login_required
def buy_page(id):
    items=Item.query.filter_by(id=int(id))[0]
    u=User.query.filter_by(username=current_user.username)[0]
    # print(items.hotel_id)
    # print(u.id)
    # print(items.price)
    
    o=Order(user_id=u.id,hotel_id=items.hotel_id)
    o.items.append(items)
    db.session.add(o)
    db.session.commit()
    return render_template('order/cart.html',o=o)   


@order_bp.route('/cart/<order_id>')
@login_required
def cart_page(order_id):
    # u=User.query.filter_by(username=current_user.username)[0]
    o = Order.query.filter_by(id=int(order_id))[0]
    oi_countdata = {}
    oi_object = OrderItemCount.query.filter_by(order_id=o.id).all()
    
    for oi_obj in oi_object:
        
        # print(f"{oi_obj.order_id}_{oi_obj.item_id}")
        oi_countdata[f"{oi_obj.order_id}_{oi_obj.item_id}"] = oi_obj.item_count
    
    # print(oi_countdata)
    # print(o.cost)
    
    return render_template('order/cart.html',o=o, oi_data=oi_countdata)   


@order_bp.route('/cart_complete/<order_id>')
@login_required
def cart_complete(order_id):
    # u=User.query.filter_by(username=current_user.username)[0]
    o = Order.query.filter_by(id=int(order_id))[0]
    o.order_completed=True
    db.session.add(o)
    db.session.commit()
    
    # print(o.cost)
    
    flash(f"Your order is compete. Thanks for shopping with us ", category='success')
    return redirect(url_for('home_page'))


@order_bp.route('/buy_order/', methods=['GET', 'POST'])
@login_required
def buy_order():
    # print('-'*50)
    if request.method == 'POST':
        # data =  request.form.to_dict()
        data = request.get_json();
        # data = None
        # print(list(data.keys()))
        
        temp_it = Item.query.filter_by(id=int(list(data.keys())[0]))[0]
        u=User.query.filter_by(username=current_user.username)[0]
        o=Order(user_id=u.id,hotel_id=temp_it.hotel_id,cost=0)
        db.session.add(o)
        db.session.commit()
        items = []
        for item_id in data:
            # print(item_id)
            it = Item.query.filter_by(id=int(item_id))[0]
            o.cost += it.price*data[item_id]
            o.items.append(it)
            ord_it_cnt = OrderItemCount(order_id = o.id, item_id = it.id, item_count = data[item_id])
            db.session.add(ord_it_cnt)
            db.session.commit()
            # print(ord_it_cnt.item_count, ord_it_cnt.item_id, ord_it_cnt.order_id, ord_it_cnt.id)
        
        # print(item.price)
        # print(o.cost)
        
        
        return json.dumps({'order_id': o.id})
    
    # print('success')
    items=Item.query.filter_by(id=1)[0]
    u=User.query.filter_by(username=current_user.username)[0]
    # print('-'*50)
    # print(items.hotel_id)
    # print(u.id)
    # print(items.price)
    
    o=Order(user_id=u.id,hotel_id=items.hotel_id,cost=0)
    db.session.add(o)
    db.session.commit()
    return render_template('order/cart.html',o=o)   


@order_bp.route('/getorder/<order_id>', methods=['GET', 'POST'])
def getorder_page(order_id):
    data = {}
    try:
        u = Order.query.filter_by(id=order_id).first()
        # u = X.query.filter_by(id=order_id).first()
        print(u)
        if u is not None:
            data['cost'] = u.cost
            data['hotel_id'] = u.hotel_id
            data['user_id'] = u.user_id
            data['order_completed'] = u.order_completed
            data['query_status'] = 200
        else:
            data['query_status'] = 404
    except Exception:
        data['query_status'] = 500
    return data