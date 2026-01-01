# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import pytest
# import bcrypt
# from app import create_app, db
# from app.models import Staff
# from app.utils.createToken import create_tokens

# @pytest.fixture(scope="session")
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#         "SECRET_KEY": "test-secret-key"
#     })

#     with app.app_context():
#         db.create_all()
#         yield app
#         db.drop_all()

    

# @pytest.fixture()
# def client(app):
#     return app.test_client()

# @pytest.fixture()
# def auth_headers(app):
#     with app.app_context():
#         password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()

#         admin = Staff(
#             name="Admin",
#             email="admin@test.com",
#             password=password,
#             isAdmin=True,
#             refreshToken="init"
#         )

#         db.session.add(admin)
#         db.session.commit()

#         access, refresh = create_tokens(admin.id)
#         admin.refreshToken = refresh
#         db.session.commit()

#         return {
#             "Authorization": f"Bearer {access}"
#         }


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import pytest
# import bcrypt
# from app import create_app, db
# from app.models import Staff
# from app.utils.createToken import create_tokens


# @pytest.fixture(scope="session")
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#         "SECRET_KEY": "test-secret-key"
#     })

#     with app.app_context():
#         db.create_all()
#         yield app
#         db.drop_all()


# @pytest.fixture(scope="function")
# def db_session(app):
#     """Creates a clean DB session for each test"""
#     with app.app_context():
#         connection = db.engine.connect()
#         transaction = connection.begin()

#         session = db.session
#         session.bind = connection

#         yield session

#         session.rollback()
#         connection.close()
#         session.remove()


# @pytest.fixture()
# def client(app, db_session):
#     return app.test_client()


# @pytest.fixture()
# def auth_headers(db_session):
#     # Check if admin already exists
#     admin = db_session.query(Staff).filter_by(email="admin@test.com").first()
    
#     if not admin:
#         password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
#         admin = Staff(
#             name="Admin",
#             email="admin@test.com",
#             password=password,
#             isAdmin=True,
#             refreshToken="init"
#         )
#         db_session.add(admin)
#         db_session.commit()
    
#     # Generate and return auth headers...


# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import pytest
# import bcrypt
# from app import create_app, db
# from app.models import Staff
# from app.utils.createToken import create_tokens


# @pytest.fixture(scope="session")
# def app():
#     test_config = {
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#         "SQLALCHEMY_TRACK_MODIFICATIONS": False,
#         "SECRET_KEY": "test-secret-key"
#     }

#     app = create_app(test_config)

#     with app.app_context():
#         db.create_all()
#         yield app
#         db.drop_all()


# @pytest.fixture(scope="function")
# def db_session(app):
#     connection = db.engine.connect()
#     transaction = connection.begin()

#     session = db.session
#     session.bind = connection

#     yield session

#     transaction.rollback()
#     connection.close()
#     session.remove()


# @pytest.fixture()
# def client(app, db_session):
#     return app.test_client()


# @pytest.fixture()
# def auth_headers(db_session):
#     password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()

#     admin = Staff(
#         name="Admin",
#         email="admin@test.com",
#         password=password,
#         isAdmin=True,
#         refreshToken="init"
#     )

#     db_session.add(admin)
#     db_session.commit()

#     access, refresh = create_tokens(admin.id)
#     admin.refreshToken = refresh
#     db_session.commit()

#     return {
#         "Authorization": f"Bearer {access}"
#     }


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import pytest
# import bcrypt
# from app import create_app, db
# from app.models import Staff
# from app.utils.createToken import create_tokens

# import pytest
# import bcrypt

# from app import create_app, db
# from app.models import Staff


# # -------------------------------
# # APP FIXTURE
# # -------------------------------
# @pytest.fixture(scope="function")
# def app():
#     app = create_app()

#     app.config.update({
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#         "SECRET_KEY": "test-secret-key"
#     })

#     with app.app_context():
#         db.drop_all()
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


# # -------------------------------
# # CLIENT FIXTURE
# # -------------------------------
# @pytest.fixture(scope="function")
# def client(app):
#     return app.test_client()


# # -------------------------------
# # DATABASE SESSION FIXTURE
# # -------------------------------
# @pytest.fixture(scope="function")
# def db_session(app):
#     yield db.session
#     db.session.rollback()


# # -------------------------------
# # AUTH HEADERS FIXTURE (JWT)
# # -------------------------------
# @pytest.fixture(scope="function")
# def auth_headers(client, db_session):
#     password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()

#     admin = Staff(
#         name="Admin",
#         email="admin@test.com",
#         password=password,
#         isAdmin=True,
#         refreshToken="init"
#     )

#     db_session.add(admin)
#     db_session.commit()

#     response = client.post(
#         "/api/v1/auth/login",
#         json={
#             "email": "admin@test.com",
#             "password": "admin123"
#         }
#     )

#     assert response.status_code == 200

#     access_token = response.json["accessToken"]

#     return {
#         "Authorization": f"Bearer {access_token}"
#     }



import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import bcrypt

from app import create_app, db
from app.models import Staff
from app.utils.createToken import create_tokens


# -----------------------------------
# APP FIXTURE
# -----------------------------------
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


# -----------------------------------
# DATABASE SESSION (ROLLBACK PER TEST)
# -----------------------------------
@pytest.fixture(scope="function")
def db_session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.session
    session.bind = connection

    yield session

    session.rollback()
    transaction.rollback()
    connection.close()
    session.remove()


# -----------------------------------
# CLIENT
# -----------------------------------
@pytest.fixture(scope="function")
def client(app, db_session):
    return app.test_client()


# -----------------------------------
# JWT HEADERS (⚠️ NOT auth_headers)
# -----------------------------------
@pytest.fixture(scope="function")
def jwt_headers(db_session):
    admin = db_session.query(Staff).filter_by(email="admin@test.com").first()

    if not admin:
        password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
        admin = Staff(
            name="Admin",
            email="admin@test.com",
            password=password,
            isAdmin=True,
            refreshToken="init"
        )
        db_session.add(admin)
        db_session.commit()

    access_token, refresh_token = create_tokens(admin.id)

    return {
        "Authorization": f"Bearer {access_token}"
    }
