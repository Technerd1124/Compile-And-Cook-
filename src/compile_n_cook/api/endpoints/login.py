from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, flash
from flask_wtf import FlaskForm
from wtforms import TelField, StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import Length, Email, EqualTo, DataRequired, Optional

LOGIN_API = Namespace('account', description='login related operations')


class MyForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=5, max=20, message="Username must be between 5 and 20 characters")
    ])

    email = EmailField('Email address', validators=[
        DataRequired(message="Email is required"),
        Email(message="Enter a valid email address")
    ])

    phone_number = TelField('Phone Number', validators=[
        DataRequired(message="Phone Number is required"),
        Length(min=10, max=10, message="Phone Number must be 10 digits")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, max=8, message="Password must be 8 characters")
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Confirm Password is required"),
        EqualTo('password', message="Passwords must match"),
        Length(min=8, max=8, message="Confirm Password must be 8 characters")
    ])

    submit = SubmitField('Submit', render_kw={'class': 'btn btn-primary'})

    def adjust_for_login(self):
        self.username.validators[:] = [Optional()]
        self.phone_number.validators[:] = [Optional()]
        self.confirm_password.validators[:] = [Optional()]

    def make_required(self):
        self.username.validators[:] = [
            DataRequired(message="Username is required"),
            Length(min=5, max=20,
                   message="Username must be between 5 and 20 characters")
        ]
        self.phone_number.validators[:] = [
            DataRequired(message="Phone Number is required"),
            Length(min=10, max=10, message="Phone Number must be 10 digits")
        ]
        self.confirm_password.validators[:] = [
            DataRequired(message="Confirm Password is required"),
            EqualTo('password', message="Passwords must match"),
            Length(min=8, max=8, message="Confirm Password must be 8 characters")
        ]


ADMIN_EMAIL = "admin@compilecook.com"
ADMIN_PASSWORD = "admin@2024"


@LOGIN_API.route('/login', methods=['GET', 'POST'])
class Login(Resource):
    def get(self):
        form = MyForm()
        form.adjust_for_login()
        return make_response(render_template('./Login/login.html', form=form))

    def post(self):
        form = MyForm()
        form.adjust_for_login()
        if form.validate_on_submit():
            from src.compile_n_cook.database.login_model import Login
            flag = False
            log = Login.query.all()
            email = form.email.data
            password = form.password.data
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                return make_response(render_template('./base.html', form=form, admin=True))
            for data in log:
                if data.email == email and data.password == password:
                    flag = True
                    break
            if flag:
                return make_response(render_template('./base.html', form=form, admin=False))
            else:
                flash('Incorrect email or password. Please try again.', 'error')
                return make_response(render_template('./Login/login.html', form=form))
        return make_response(render_template('./Login/login.html', form=form))


@LOGIN_API.route('/signup', methods=['GET', 'POST'])
class SignUp(Resource):
    def get(self):
        form = MyForm()
        form.make_required()
        return make_response(render_template('./Login/signup.html', form=form))

    def post(self):
        from src.compile_n_cook.database import db
        from src.compile_n_cook.database.login_model import Login
        form = MyForm()
        form.make_required()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            phone_no = int(form.phone_number.data)
            password = form.password.data

            login = Login(username=username, email=email,
                          phone_no=phone_no, password=password)

            db.session.add(login)
            db.session.commit()
            return make_response(render_template('./Login/login.html', form=form))
        return make_response(render_template('./Login/signup.html', form=form))
