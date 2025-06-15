from flask import render_template, request, redirect, url_for, jsonify
from . import db
from .models import User, Student, Event

def init_routes(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return render_template('index.html', current="index")
    
    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', current="users", users=users)

    @app.route('/user/add', methods=["GET", "POST"])
    def user_add():
        if request.method == "GET":
            return render_template('user/add.html', current="users")
        if request.method == "POST":
            user = User()
            user.username = request.form["username"]
            user.password = request.form["password"]
            db.session.add(user)
            db.session.commit()
            return redirect("/users")

    @app.route('/user/edit/<id>', methods=["GET", "POST"])
    def user_edit(id):
        if request.method == "GET":
            user = db.get_or_404(User, id)
            return render_template('user/edit.html', current="users", user=user)
        if request.method == "POST":
            user = db.get_or_404(User, request.form["id"])
            user.username = request.form["username"]
            user.password = request.form["password"]
            db.session.commit()
            return redirect("/users")

    @app.route('/user/del/<id>', methods=["GET", "POST"])
    def user_del(id):
        if request.method == "GET":
            user = db.get_or_404(User, id)
            return render_template('user/del.html', current="users", user=user)
        if request.method == "POST":
            user = db.get_or_404(User, request.form["id"])
            db.session.delete(user)
            db.session.commit()
            return redirect("/users")

    @app.route('/students')
    def students():
        students = Student.query.all()
        return render_template('students.html', current="students", students=students)

    @app.route('/student/add', methods=["GET", "POST"])
    def student_add():
        if request.method == "GET":
            return render_template('student/add.html', current="students")
        if request.method == "POST":
            student = Student()
            student.first_name = request.form["first-name"]
            student.last_name = request.form["last-name"]
            student.patronymic = request.form["patronymic"]
            student.group = request.form["group"]
            db.session.add(student)
            db.session.commit()
            return redirect("/students")

    @app.route('/student/edit/<id>', methods=["GET", "POST"])
    def student_edit(id):
        if request.method == "GET":
            student = db.get_or_404(Student, id)
            return render_template('student/edit.html', current="students", student=student)
        if request.method == "POST":
            student = db.get_or_404(Student, request.form["id"])
            student.first_name = request.form["first-name"]
            student.last_name = request.form["last-name"]
            student.patronymic = request.form["patronymic"]
            student.group = request.form["group"]
            db.session.commit()
            return redirect("/students")

    @app.route('/student/del/<id>', methods=["GET", "POST"])
    def student_del(id):
        if request.method == "GET":
            student = db.get_or_404(Student, id)
            return render_template('student/del.html', current="students", student=student)
        if request.method == "POST":
            student = db.get_or_404(Student, request.form["id"])
            db.session.delete(student)
            db.session.commit()
            return redirect("/students")

    @app.route('/events')
    def events():
        events = Event.query.all()
        return render_template('events.html', current="events", events=events)