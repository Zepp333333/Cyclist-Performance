#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pytest


def test_home_page(client):
    """
    GIVEN a Flask app configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask Blog" in response.data


def test_home_page_post(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post('/')
    assert response.status_code == 405
    assert b"Flask Blog!" not in response.data


# def test_register_authenticated_user(test_client):
#     """
#     GIVEN a Flask app configured for testing and mock-up authenticated user
#     WHEN the '/register' page is requested (GET)
#     THEN check the response is valid and being redirected to '/index'
#     """
#     with test_client.session_transaction() as session:
#         session['user'] = {'email': 'Sergey@mail.ru'}
#
#     response = test_client.get('/register', follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Flask Blog" in response.data
#     assert b"Join Today" not in response.data


def test_register(client):
    """
    GIVEN a Flask app configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Join Today" in response.data


# def test_register_post(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' page is is posted to (POST)
#     THEN check that a '405' status code is returned
#     """
#     response = test_client.post('/register')
#     assert response.status_code == 405
#     assert b"Flask Blog!" not in response.data



def test_valid_login_redirect_logout(client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    # response = test_client.post('/login',
    #                             data=dict(email='patkennedy79@gmail.com', password='FlaskIsAwesome'),
    #                             follow_redirects=True)


    client.post('/login', data=dict(email='ssa@mail.ru', password='123'))
    response = client.get('/')
    assert response.status_code == 200

    assert b"Logout" in response.data
    assert b"Account" in response.data
    assert b"Login" not in response.data
    assert b"Register" not in response.data
#
#     """
#     GIVEN a Flask application
#     WHEN the '/logout' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/logout', follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Logout" not in response.data
#     assert b"Login" in response.data
#     assert b"Register" in response.data
