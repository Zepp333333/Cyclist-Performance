#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pytest
import sqlalchemy
from sqlalchemy.orm import close_all_sessions
from cycperf import create_app
from flask_migrate import upgrade

from config import ConfigTest

TEST_DB_NAME = ConfigTest.TEST_DB_NAME


@pytest.fixture(scope='function')
def create_db_connection():
    # todo add docstring
    connection = sqlalchemy.create_engine(ConfigTest.SQLALCHEMY_DATABASE_URI,
                                          isolation_level="AUTOCOMMIT").connect()
    yield connection
    # Tear down
    connection.close()


@pytest.fixture(scope='module')
def create_test_db():
    # todo add docstring
    def _create_test_db():
        with sqlalchemy.create_engine(ConfigTest.TEST_DATABASE_SERVER,
                                      isolation_level="AUTOCOMMIT").connect() as connection:
            connection.execute(f'CREATE DATABASE {TEST_DB_NAME}')

    yield _create_test_db()

    # Tear down
    def _drop_test_db():
        with sqlalchemy.create_engine(ConfigTest.TEST_DATABASE_SERVER,
                                      isolation_level="AUTOCOMMIT").connect() as connection:
            close_all_sessions()
            connection.execute(f'DROP DATABASE {TEST_DB_NAME} WITH (FORCE)')

    _drop_test_db()


# @pytest.fixture(scope='session')
# def create_test_db():
#     # todo add docstring
#     def _create_test_db():
#         with sqlalchemy.create_engine("postgresql://postgres@localhost",
#                                       isolation_level="AUTOCOMMIT").connect() as connection:
#             connection.execute(f'CREATE DATABASE {TEST_DB_NAME}')
#
#     yield _create_test_db()

# # Tear down
# def _drop_test_db():
#     print("_in _drop_test_db")
#     with sqlalchemy.create_engine("postgresql://postgres@localhost",
#                                   isolation_level="AUTOCOMMIT").connect() as connection:
#         close_all_sessions()
#         connection.execute(f'DROP DATABASE {TEST_DB_NAME} WITH (FORCE)')
#
# _drop_test_db()


@pytest.fixture(scope='module')
def test_client(create_test_db):
    # todo add docstring
    _app = create_app(ConfigTest)
    with _app.app_context():
        upgrade()
    testing_client = _app.test_client()
    ctx = _app.app_context()
    ctx.push()
    yield testing_client
    # Tear down
    ctx.pop()

# @pytest.fixture(scope='module')
# def flask_app():
#     app = create_app()
#     app.config.from_object(ConfigTest)
#     with app.app_context():
#         yield app
#
#
# @pytest.fixture(scope='module')
# def client(flask_app):
#     app = flask_app
#     ctx = flask_app.test_request_context()
#     ctx.push()
#     app.test_client_class = FlaskClient
#     return app.test_client()

# @pytest.fixture(scope='module')
# def test_client():
#     app = create_app(ConfigTest)
#
#     with app.test_client() as testing_client:
#         with app.app_context():
#             yield testing_client
#
#
# @pytest.fixture()
# def test_with_authenticated_user(app):
#     @login_manager.request_loader
#     def load_user_from_request(request):
#         return Users.query.first()
#
#
# @pytest.fixture(scope='module')
# def init_database():
#     # Create the database and the database table
#     db.create_all()
#
#     # Insert user data
#     user1 = Users(username='pat',
#                  email='patkennedy79@gmail.com',
#                  password=bcrypt.generate_password_hash('FlaskIsAwesome').decode('utf-8'))
#     user2 = Users(username='fam', email='kennedyfamilyrecipes@gmail.com', password='PaSsWoRd')
#     db.session.add(user1)
#     db.session.add(user2)
#
#     # Commit the changes for the users
#     db.session.commit()
#
#     yield db  # this is where the testing happens!
#
#     db.drop_all()
#
#
#
# @pytest.fixture(scope='module')
# def new_user():
#     return Users(username='Vasya', email='vasya@mail.ru', password='123456')


# @pytest.fixture
# def authenticated_request(app):
#     with app.test_request_context():
#         yield flask_login.login_user(Users(email='Sergey@mail.ru'))
