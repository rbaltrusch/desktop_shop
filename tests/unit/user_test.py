# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 17:25:46 2021

@author: richa
"""

# pylint: skip-file

from desktop_shop import user


def test_capitalized():
    user_data = user.UserData(first_name="john", last_name="miller")
    assert user_data.first_name == "John"
    assert user_data.last_name == "Miller"


def test_full_name():
    user_data = user.UserData(first_name="john", last_name="miller")
    assert user_data.full_name == "John Miller"


def test_user_data_list_conversion():
    user_data = user.UserData(
        first_name="john",
        last_name="miller",
        dob="1991",
        email="john@example.com",
        gender="m",
    )
    user_data_list = list(user_data)
    assert len(user_data_list) == 5
    first_name, last_name, gender, dob, email = user_data_list
    assert first_name == user_data.first_name
    assert last_name == user_data.last_name
    assert gender == user_data.gender
    assert dob == user_data.dob
    assert email == user_data.email


def test_sign_up_user_data():
    user_data = user.UserSignUpData(
        first_name="john",
        last_name="miller",
        dob="1991",
        email="john@example.com",
        gender="m",
        join_date="2021",
    )
    user_data_list = list(user_data)
    assert len(user_data_list) == 6
    first_name, last_name, gender, dob, email, join_date = user_data_list
    assert first_name == user_data.first_name
    assert last_name == user_data.last_name
    assert gender == user_data.gender
    assert dob == user_data.dob
    assert email == user_data.email
    assert join_date == user_data.join_date


def test_getitem():
    user_data = user.UserData(first_name="john", last_name="miller")
    assert user_data[0] == user_data.first_name
