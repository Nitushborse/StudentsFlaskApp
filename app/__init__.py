from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)

    with app.app_context():
        from app.auth.authRoutes import auth_bp
        from app.staff.staffRoutes import staff_bp
        from app.student.studentRoutes import student_bp


        app.register_blueprint(auth_bp, url_prefix="/api/v1")
        app.register_blueprint(staff_bp, url_prefix="/api/v1")
        app.register_blueprint(student_bp, url_prefix="/api/v1")
        db.create_all()

    return app