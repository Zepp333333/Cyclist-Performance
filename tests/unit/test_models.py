#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, email and password are defined correctly
    """
    assert new_user.email == 'vasya@mail.ru'
    assert new_user.username == 'Vasya'
    assert new_user.password == '123456'



# def test_load_user():
#     assert False
#
#
# def test_user():
#     assert False
#
#
# def test_dbactivity():
#     assert False
