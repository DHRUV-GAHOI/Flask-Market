from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import *
from market.forms import RegisterForm, LoginForm,Itemform
from market.forms import RegisterForm, LoginForm ,HotelForm
from market import db
import json
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    print('dfdfsd')
    items = Hotel.query.all()
    print(items)
    return render_template('market.html', items=items)

@app.route('/menu/<id>')
@login_required
def menu(id):
    print('laura')
    print(id)
    items=Item.query.filter_by(hotel_id=int(id))
    print('sucess'*100)
    print(items[0])
    return render_template('menu.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/buy_page/<id>')
@login_required
def buy_page(id):
    print('success')
    items=Item.query.filter_by(id=int(id))[0]
    print('abcd')
    u=User.query.filter_by(username=current_user.username)[0]
    print('sdd'*100)
    print(items.hotel_id)
    print(u.id)
    print(items.price)
    
    o=Order(user_id=u.id,hotel_id=items.hotel_id)
    o.items.append(items)
    db.session.add(o)
    db.session.commit()
    return render_template('cart.html',o=o)   


@app.route('/cart/<order_id>')
@login_required
def cart_page(order_id):
    # u=User.query.filter_by(username=current_user.username)[0]
    o = Order.query.filter_by(id=int(order_id))[0]
    print(o.cost)
    return render_template('cart.html',o=o)   

@app.route('/cart_complete/<order_id>')
@login_required
def cart_complete(order_id):
    # u=User.query.filter_by(username=current_user.username)[0]
    o = Order.query.filter_by(id=int(order_id))[0]
    o.order_completed=True
    db.session.add(o)
    db.session.commit()
    
    print(o.cost)
    
    flash(f"Your order is compete. Thanks for shopping with us ", category='success')
    return redirect(url_for('home_page'))

@app.route('/buy_order/', methods=['GET', 'POST'])
@login_required
def buy_order():
    print('-'*50)
    if request.method == 'POST':
        # data =  request.form.to_dict()
        data = request.get_json();
        # data = None
        print(data)
        
        items = []
        for item_id in data:
            print(item_id)
            for _ in ' '*data[item_id]:
                items.append(Item.query.filter_by(id=int(item_id))[0])
            
        print(items)    
        u=User.query.filter_by(username=current_user.username)[0]
        o=Order(user_id=u.id,hotel_id=items[0].hotel_id,cost=0)
        
        for item in items:
            o.items.append(item)
            o.cost += item.price
        # print(item.price)
        print(o.cost)
        db.session.add(o)
        db.session.commit()
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
    return render_template('cart.html',o=o)   


@app.route('/item_input', methods=['GET', 'POST'])
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
    return render_template('item_input.html', form=form)

@app.route('/hotel_input', methods=['GET', 'POST'])
def hotel_input_page():
    form = HotelForm()
    if form.validate_on_submit():
        hotel_to_create = Hotel(name=form.name.data,
                              description=form.description.data,
                              location=form.location.data)
        db.session.add(hotel_to_create)
        db.session.commit()
        flash(f"Account created successfully! You are now logged in as {hotel_to_create.name}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    # return render_template('item_input.html', form=form)
    return render_template('hotel_input.html', form=form)



@app.route('/add_to_cart/<id>')
@login_required
def add_to_cart(id):
    print('success')
    items=Item.query.filter_by(id=int(id))[0]
    print('abcd')
    u=User.query.filter_by(username=current_user.username)[0]
    print('sdd'*100)
    print(items.hotel_id)
    print(u.id)
    print(items.price)
    
    o=Order(user_id=u.id,hotel_id=items.hotel_id)
    o.items.append(items)
    db.session.add(o)
    db.session.commit()
    return render_template('cart.html',o=o)    
    

