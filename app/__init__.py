from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate
from .config import DevelopmentConfig  # или ProductionConfig

# Загрузка .env должна происходить до создания приложения
load_dotenv()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Регистрация маршрутов
    from . import routes
    routes.init_routes(app)
    
    return app