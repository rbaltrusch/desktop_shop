# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 18:29:09 2021

@author: richa
"""

import os
import sqlite3
import pytest

import server
import database

DATABASE = 'main2.db'
cursor = None

def setup():
    global cursor
    cursor = sqlite3.connect(DATABASE)
    database.create_user_table(cursor)
    database.create_sessions_table(cursor)

def teardown():
    cursor.close()
    try:
        if os.path.isfile(DATABASE):
            os.remove(DATABASE)
    except PermissionError:
        pass

@pytest.mark.slow
@pytest.mark.usefixtures("user_sign_up_data")
@pytest.mark.usefixtures("password")
def test_add_user(user_sign_up_data, password):
        session_id = server.add_user(cursor, user_sign_up_data, password)
        verified = database.verify_session_id_by_user_email(cursor, session_id, user_sign_up_data.email)
        assert verified

        _, user_data_stored = server.query_user_data(cursor,
                                                     user_sign_up_data.email,
                                                     user_email=user_sign_up_data.email,
                                                     session_id=session_id
                                                     )
        assert user_data_stored == list(user_sign_up_data)

@pytest.mark.slow
@pytest.mark.usefixtures("user_sign_up_data")
@pytest.mark.usefixtures("password")
@pytest.mark.usefixtures("pepper")
def test_login(user_sign_up_data, password, pepper):
        database.add_user(cursor, user_sign_up_data, password, pepper=pepper)
        session_id = server.login(cursor, user_sign_up_data.email, password)
        verified = database.verify_session_id_by_user_email(cursor, session_id, user_sign_up_data.email)
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
