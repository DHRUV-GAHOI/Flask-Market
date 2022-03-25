from market.app import db, app
from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.models import *
from market.forms import RegisterForm, LoginForm, Itemform, HotelForm
import json
from flask_login import login_user, logout_user, login_required, current_user

restaurant_bp = Blueprint('restaurant_bp', __name__, template_folder='templates')

@restaurant_bp.route('/market')
@login_required
def market_page():
    items = Hotel.query.all()
    # print(items)
    return render_template('restaurant/market.html', items=items)


@restaurant_bp.route('/menu/<rest_id>')
@login_required
def menu(rest_id):
    # print(rest_id)
    items=Item.query.filter_by(hotel_id=int(rest_id))
    # print(items[0])
    return render_template('restaurant/menu.html', items=items)


@restaurant_bp.route('/item_input', methods=['GET', 'POST'])
def item_input_page():
    form = Itemform()
    if form.validate_on_submit():
        item_to_create = Item(name=form.name.data,
                              description=form.description.data,
                              price=form.price.data,
                              hotel_id=form.hotel_id.data)
        db.session.add(item_to_create)
        db.session.commit()
        flash(f"Account created successfully! You are now logged in as {item_to_create.name}", category='success')
    return render_template('restaurant/item_input.html', form=form)


@restaurant_bp.route('/hotel_input', methods=['GET', 'POST'])
def hotel_input_page():
    form = HotelForm()
    if form.validate_on_submit():
        hotel_to_create = Hotel(name=form.name.data,
                              description=form.description.data,
                              location=form.location.data)
        db.session.add(hotel_to_create)
        db.session.commit()
        flash(f"Account created successfully! You are now logged in as {hotel_to_create.name}", category='success')
        # return redirect(url_for('restaurant_bp.market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    # return render_template('item_input.html', form=form)
    return render_template('restaurant/hotel_input.html', form=form)


@restaurant_bp.route('/getitem/<item_id>', methods=['GET', 'POST'])
def getitem_page(item_id):
    data = {}
    try:
        u = Item.query.filter_by(id=item_id).first()
        print(u)
        if u is not None:
            data['name'] = u.name
            data['price'] = u.price
            data['hotel_id'] = u.hotel_id
            data['description'] = u.description
            data['query_status'] = 200
        else:
            data['query_status'] = 404
    except Exception:
        data['query_status'] = 500
    return data


@restaurant_bp.route('/gethotel/<hotel_id>', methods=['GET', 'POST'])
def gethotel_page(hotel_id):
    data = {}
    try:
        u = Hotel.query.filter_by(id=hotel_id).first()
        print(u)
        if u is not None:
            data['name'] = u.name
            data['location'] = u.location
            data['description'] = u.description
            data['query_status'] = 200
        else:
            data['query_status'] = 404
    except Exception:
        data['query_status'] = 500
    return data