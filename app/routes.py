from flask import render_template, request, redirect, url_for, jsonify
from . import db
from .models import User

def init_routes(app):
    @app.route('/')
    def index():
        return 'Главная страница'
    
    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', users=users)