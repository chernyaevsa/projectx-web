import os
from flask import render_template, request, redirect, url_for, jsonify, flash, send_file, make_response
from . import db
from .models import User, Student, Event
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

def init_routes(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return render_template('index.html', current="index")
    
    @app.route('/users')
    @login_required
    def users():
        users = User.query.all()
        return render_template('users.html', current="users", users=users)

    @app.route('/user/add', methods=["GET", "POST"])
    @login_required
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
    @login_required
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
    @login_required
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
    @login_required
    def students():
        students = Student.query.all()
        return render_template('students.html', current="students", students=students)

    @app.route('/student/add', methods=["GET", "POST"])
    @login_required
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
    @login_required
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
    @login_required
    def student_del(id):
        if request.method == "GET":
            student = db.get_or_404(Student, id)
            return render_template('student/del.html', current="students", student=student)
        if request.method == "POST":
            student = db.get_or_404(Student, request.form["id"])
            db.session.delete(student)
            db.session.commit()
            return redirect("/students")
    
    @app.route('/student/photo-edit/<id>', methods=["GET", "POST"])
    def student_photo_edit(id):
        if request.method == "GET":
            student = db.get_or_404(Student, id)
            return render_template('student/add_photo.html', current="students", student=student)
        if request.method == "POST":
            print("Hi")
            # Проверяем, есть ли файл в запросе
            if 'photo' not in request.files:
                flash('No file part')
                return redirect("/students")
        
            file = request.files['photo']
            print(file)
        
            # Если пользователь не выбрал файл
            if file.filename == '':
                flash('No selected file')
                return redirect("/students")
            
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"jpg"}
            
            # Если файл разрешен и корректен
            if file and allowed_file(file.filename):
                if not os.path.exists(app.config['IMGS']):
                    os.makedirs(app.config['IMGS'])
                file.save(os.path.abspath(os.path.join(app.config['IMGS'], f"{id}.jpg")))
                return redirect("/students")
    
        return redirect("/students")

    @app.route('/student/photo/<id>', methods=["GET", "POST"])
    def student_photo(id):
        if request.method == "GET":
            student = db.get_or_404(Student, id)
            if os.path.isfile(os.path.join(app.config['IMGS'], f"{id}.jpg")):
                return send_file(os.path.abspath(os.path.join(app.config['IMGS'], f"{id}.jpg")), as_attachment=True)
            else:
                return make_response(f"File '{id}' not found.", 404)
    
    @app.route('/students/json')
    def students_all():
        students = Student.query.all()
        result = []
        for student in students:
            student_dict = student.__dict__
            student_dict.pop('_sa_instance_state', None)  # Удаляем служебное поле SQLAlchemy
            result.append(student_dict)
        return jsonify(result)

    @app.route('/events')
    @login_required
    def events():
        events = Event.query.all()
        
        return render_template('events.html', current="events", events=events)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        
            user = User.query.filter_by(username=username, password=password).first()
            
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect("/")
            else:
                flash('Неверное имя пользователя или пароль', 'danger')
    
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")