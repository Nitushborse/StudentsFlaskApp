# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# import os

# load_dotenv()

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#     db.init_app(app)

#     with app.app_context():
#         from app.auth.authRoutes import auth_bp
#         from app.staff.staffRoutes import staff_bp
#         from app.student.studentRoutes import student_bp


#         app.register_blueprint(auth_bp, url_prefix="/api/v1")
#         app.register_blueprint(staff_bp, url_prefix="/api/v1")
#         app.register_blueprint(student_bp, url_prefix="/api/v1")
#         db.create_all()

#     return app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    # ---------- CONFIG ----------
    if test_config is not None:
        # Used by pytest (SQLite, test secret, etc.)
        app.config.update(test_config)
    else:
        # Used by normal run (MySQL / production)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Ensure defaults even in tests
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('SECRET_KEY', os.getenv('SECRET_KEY', 'dev-secret'))

    CORS(
        app,
        resources={r"/api/*": {"origins": os.getenv('FRONTEND_URL')}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # ---------- INIT DB ----------
    db.init_app(app)
    migrate.init_app(app, db)
    # ---------- REGISTER BLUEPRINTS ----------
    from app.auth.authRoutes import auth_bp
    from app.staff.staffRoutes import staff_bp
    from app.student.studentRoutes import student_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(staff_bp, url_prefix="/api/v1")
    app.register_blueprint(student_bp, url_prefix="/api/v1")

    # ---------- CREATE TABLES ----------
    # with app.app_context():
    #     db.create_all()

    return app
