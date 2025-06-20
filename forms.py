from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    role = SelectField("Role", choices=[
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
        ('delivery', 'Delivery')
    ])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class FoodForm(FlaskForm):
    name = StringField("Food Name", validators=[InputRequired()])
    price = FloatField("Price", validators=[InputRequired()])
    submit = SubmitField("Add Food")
