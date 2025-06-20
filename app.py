# app.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, User, FoodItem, Order
from forms import RegisterForm, LoginForm, FoodForm

app = Flask(__name__)
app.secret_key = 'food123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            flash("Login successful")
            if user.role == 'admin':
                return redirect(url_for('dashboard_admin'))
            elif user.role == 'seller':
                return redirect(url_for('dashboard_seller'))
            elif user.role == 'customer':
                return redirect(url_for('dashboard_customer'))
            else:
                return redirect(url_for('dashboard_delivery'))
        flash("Invalid credentials")
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))

@app.route('/dashboard/admin')
def dashboard_admin():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('dashboard_admin.html')

@app.route('/dashboard/seller', methods=['GET', 'POST'])
def dashboard_seller():
    if session.get('role') != 'seller':
        return redirect(url_for('login'))
    form = FoodForm()
    if form.validate_on_submit():
        food = FoodItem(name=form.name.data, price=form.price.data, seller_id=session['user_id'])
        db.session.add(food)
        db.session.commit()
        flash("Food added!")
    foods = FoodItem.query.filter_by(seller_id=session['user_id']).all()
    return render_template('dashboard_seller.html', form=form, foods=foods)

@app.route('/dashboard/customer')
def dashboard_customer():
    if session.get('role') != 'customer':
        return redirect(url_for('login'))
    foods = FoodItem.query.all()
    return render_template('dashboard_customer.html', foods=foods)

@app.route('/order/<int:food_id>')
def order_food(food_id):
    if session.get('role') != 'customer':
        return redirect(url_for('login'))
    order = Order(food_id=food_id, customer_id=session['user_id'], status='Pending')
    db.session.add(order)
    db.session.commit()
    flash("Order placed!")
    return redirect(url_for('dashboard_customer'))

@app.route('/dashboard/delivery')
def dashboard_delivery():
    if session.get('role') != 'delivery':
        return redirect(url_for('login'))
    orders = Order.query.all()
    return render_template('dashboard_delivery.html', orders=orders)

@app.route('/deliver/<int:order_id>')
def deliver_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'Delivered'
    db.session.commit()
    flash("Order marked as delivered")
    return redirect(url_for('dashboard_delivery'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
