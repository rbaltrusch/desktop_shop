# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 18:29:09 2021

@author: richa
"""

# pylint: skip-file

import os
import random
import sqlite3
import string

import pytest
from desktop_shop import database, server

cursor = None


def setup():
    global cursor, database_
    database_ = "".join(random.choices(string.ascii_lowercase, k=10)) + ".db"
    cursor = sqlite3.connect(database_)
    database.create_user_table(cursor)
    database.create_sessions_table(cursor)


def teardown():
    cursor.close()
    try:
        if os.path.isfile(database_):
            os.remove(database_)
    except PermissionError:
        pass


@pytest.mark.slow
@pytest.mark.usefixtures("user_sign_up_data")
@pytest.mark.usefixtures("password")
def test_add_user(user_sign_up_data, password):
    session_id = server.add_user(cursor, user_sign_up_data, password)
    verified = database.verify_session_id_by_user_email(
        cursor, session_id, user_sign_up_data.email
    )
    assert verified

    _, user_data_stored = server.query_user_data(
        cursor,
        user_sign_up_data.email,
        user_email=user_sign_up_data.email,
        session_id=session_id,
    )
    assert user_data_stored == list(user_sign_up_data)


@pytest.mark.slow
@pytest.mark.usefixtures("user_sign_up_data")
@pytest.mark.usefixtures("password")
@pytest.mark.usefixtures("pepper")
def test_login(user_sign_up_data, password, pepper):
    database.add_user(cursor, user_sign_up_data, password, pepper=pepper)
    session_id = server.login(cursor, user_sign_up_data.email, password)
    verified = database.verify_session_id_by_user_email(
        cursor, session_id, user_sign_up_data.email
    )
    assert verified


@pytest.mark.slow
@pytest.mark.usefixtures("user_sign_up_data")
@pytest.mark.usefixtures("password")
@pytest.mark.usefixtures("wrong_password")
@pytest.mark.usefixtures("pepper")
def test_login_failed(user_sign_up_data, password, wrong_password, pepper):
    database.add_user(cursor, user_sign_up_data, password, pepper=pepper)
    session_id = server.login(cursor, user_sign_up_data.email, wrong_password)
    assert session_id is None
