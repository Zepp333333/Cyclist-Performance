#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pytest
from cycperf.models import User
from config import ConfigTest

from cycperf import create_app


@pytest.fixture(scope='module')
def test_client():
    app = create_app(ConfigTest)

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def new_user():
    return User(username='Vasya', email='vasya@mail.ru', password='123456')


