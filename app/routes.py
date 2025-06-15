from flask import render_template, request, redirect, url_for, jsonify
from . import db
from .models import User, Student, Event

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', current="index")
    
    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', current="users", users=users)

    @app.route('/students')
    def students():
        students = Student.query.all()
        return render_template('students.html', current="students", students=students)

    @app.route('/events')
    def events():
        events = Event.query.all()
        return render_template('events.html', current="events", events=events)