import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from src.compile_n_cook.api.endpoints import AUTH_BLUEPRINT
from src.compile_n_cook.database import db
from src.compile_n_cook.database.login_model import Login
import json


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = "Syntax_Eat"
    bootstrap = Bootstrap(app)

    @app.route('/')
    def index():
        return redirect(url_for('log.account_login'))

    @app.route('/home')
    def home():
        return render_template('base.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/features')
    def features():
        return render_template('features.html')

    @app.route('/menu')
    def menu():
        try:
            with open("./src/compile_n_cook/static/scripts/breakfast.json", 'r') as b_fast:
                breakfast = json.load(b_fast)
            with open("./src/compile_n_cook/static/scripts/lunch.json", 'r') as l_all:
                lunch = json.load(l_all)
            with open("./src/compile_n_cook/static/scripts/desert.json", 'r') as d_all:
                desert = json.load(d_all)
        except FileNotFoundError:
            print("file not found")
            
        else:
            breakfast_vegetarian = breakfast['menu_items']['vegetarian']
            breakfast_beverages = breakfast['menu_items']['beverages']

            lunch_vegetarian = lunch['menu_items']['vegetarian']
            lunch_non_vegetarian = lunch['menu_items']['non_vegetarian']
            desert_india = desert['menu_items']['indian_desserts']


        return render_template('menu.html', b_veg=breakfast_vegetarian, b_bev=breakfast_beverages,l_veg=lunch_vegetarian, l_nveg=lunch_non_vegetarian, dessert=desert_india )


# DataBase Configuration - My DB name = compile_and_cook , pswrd: admin24

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin24@localhost:5432/compile_and_cook'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db, directory=os.path.join("src", "compile_n_cook", "alembic"))

    app.register_blueprint(AUTH_BLUEPRINT)
        
    return app
