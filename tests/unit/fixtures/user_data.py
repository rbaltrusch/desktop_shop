# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 21:34:17 2021

@author: richa
"""
import pytest

from desktop_shop import user, util


@pytest.fixture
def user_sign_up_data():
    return user.UserSignUpData(
        first_name="john",
        last_name="miller",
        email="john@example.com",
        join_date=util.get_current_date(),
    )


@pytest.fixture
def user_data():
    return user.UserData(
        first_name="john",
        last_name="miller",
        email="john@example.com",
    )


@pytest.fixture
def password():
    return "password3"


@pytest.fixture
def wrong_password():
    return "somethingelse"
