# -*- coding: utf-8 -*-
"""Tests for the gui callbacks module

This mostly tests happy paths and does not extensively test gui data
and look.
"""

# pylint: disable=missing-function-docstring

import os
import sys

import sqlite3
import pytest

# fix for headless machines
display = None  # pylint: disable=invalid-name
if sys.platform.startswith("linux") and os.environ.get("DISPLAY") is None:
    from pyvirtualdisplay import Display

    display = Display(visible=False, size=(100, 60))
    display.start()

# pylint: disable=wrong-import-position
from desktop_shop.gui import callbacks, init
from desktop_shop import gui, server
from desktop_shop.user import UserSignUpData
from desktop_shop.datagen import generate_data

TEST_DB = "file:cachedb?mode=memory&cache=shared"
PASSWORD = "password123"
EMAIL = "a@b.c"
ITERATIONS = 1


def teardown():
    if display is not None:
        display.stop()


def init_gui(monkeypatch: pytest.MonkeyPatch):
    generate_data.generate(
        TEST_DB,
        hash_iterations=ITERATIONS,
        transactions=1,
        users=1,
        products=1,
        sessions=1,
    )

    with sqlite3.connect(TEST_DB) as cursor:
        monkeypatch.setattr(gui, "db_conn", cursor)
        init.init()


def get_error_message() -> str:
    return gui.app["main_menu"]["error_message_label"].get_var()


def assert_no_error_message():
    assert not get_error_message()


def assert_logged_out():
    assert not gui.app.data["cart"]
    assert gui.app.data["session_id"] is None
    # assert gui.app.data["user_data"] == UserSignUpData()
    assert not gui.app.data["pw_hash"]


def assert_logged_in():
    assert gui.app.data["session_id"] is not None
    assert gui.app["home"].active
    assert gui.app["main_menu"].active


def _mock_get_user_data():
    return UserSignUpData(
        first_name="fn",
        last_name="ln",
        gender="m",
        dob="2000-01-01",
        email=EMAIL,
        join_date="2020/04/03",
    )


def _mock_register_gui(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gui.app["register"], "get_user_data", _mock_get_user_data)
    monkeypatch.setattr(gui.app["register"]["pw_entry"], "get_var", lambda: PASSWORD)
    monkeypatch.setattr(gui.app["register"]["confirm_pw_entry"], "get_var", lambda: PASSWORD)


@pytest.mark.slow
def test_register(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    with sqlite3.connect(TEST_DB) as cursor:
        monkeypatch.setattr(gui, "db_conn", cursor)
        _mock_register_gui(monkeypatch)
        callbacks.switch_to_register()
        callbacks.register()

    assert_logged_in()
    assert_no_error_message()


@pytest.mark.slow
def test_register_twice(monkeypatch: pytest.MonkeyPatch):
    test_register(monkeypatch)
    with pytest.raises(server.DuplicateUserError):
        test_register(monkeypatch)


@pytest.mark.slow
def test_sign_out(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    assert_logged_out()
    test_register(monkeypatch)
    callbacks.sign_out()
    assert_logged_out()


@pytest.mark.slow
def test_login(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    assert_logged_out()
    test_register(monkeypatch)
    callbacks.sign_out()
    assert_logged_out()
    callbacks.login(PASSWORD, EMAIL)
    assert_logged_in()


@pytest.mark.slow
def test_navigation(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    assert_logged_out()
    test_register(monkeypatch)

    callbacks.switch_to_checkout()
    assert gui.app["checkout"].active
    assert gui.app["main_menu"].active

    callbacks.switch_to_home()
    assert gui.app["home"].active
    assert gui.app["main_menu"].active

    callbacks.switch_to_profile()
    assert gui.app["profile"].active
    assert gui.app["main_menu"].active

    callbacks.sign_out()
    callbacks.switch_to_login()
    assert gui.app["login"].active
    assert gui.app["main_menu"].active


@pytest.mark.slow
def test_edit_user_data(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    test_register(monkeypatch)
    monkeypatch.setattr(gui.app["profile"], "get_user_data", _mock_get_user_data)
    callbacks.edit_user_data()
    assert_logged_in()


@pytest.mark.slow
def test_edit_user_password(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    test_register(monkeypatch)
    new_password = "234343834834"
    monkeypatch.setattr(gui.app["profile"]["pw_entry"], "get_var", lambda: new_password)
    monkeypatch.setattr(gui.app["profile"]["confirm_pw_entry"], "get_var", lambda: new_password)
    callbacks.edit_user_password()
    assert_logged_in()


@pytest.mark.slow
def test_store_user_data_error(monkeypatch: pytest.MonkeyPatch):
    init_gui(monkeypatch)
    callbacks.store_user_data(user_data=[])
    assert get_error_message().startswith("Something went wrong")


@pytest.mark.slow
@pytest.mark.parametrize(
    "user_data, expected_message_start, expected",
    [
        (UserSignUpData(first_name="a", last_name="b"), "Email", False),
        (UserSignUpData(email="a@b.c", first_name="1eer3", last_name="2aa4"), "First", False),
        (UserSignUpData(email="a@b.c", first_name="john", last_name="2bbere4 "), "Last", False),
        (UserSignUpData(email="a@b.c", first_name="john", last_name="doe"), "", True),
        (
            UserSignUpData(email="a@b.c", first_name="john", last_name="doe", gender="e"),
            "Gender",
            False,
        ),
        (
            UserSignUpData(email="a@b.c", first_name="john", last_name="doe", gender="m"),
            "",
            True,
        ),
        (
            UserSignUpData(
                email="a@b.c", first_name="john", last_name="doe", gender="m", dob="20-01-01"
            ),
            "Date of birth",
            False,
        ),
        (
            UserSignUpData(
                email="a@b.c", first_name="john", last_name="doe", gender="m", dob="2000-01-01"
            ),
            "",
            True,
        ),
    ],
)
def test_validate_user_data(
    monkeypatch: pytest.MonkeyPatch, user_data, expected_message_start, expected
):
    init_gui(monkeypatch)
    assert callbacks.validate_user_data(user_data) == expected
    if expected_message_start:
        assert get_error_message().startswith(expected_message_start)


@pytest.mark.slow
@pytest.mark.parametrize(
    "password, confirm_password, expected_message, expected",
    [
        ("a", "a", "Password needs to be at least 8 characters long.", False),
        ("123456789", "qwewewewwewew", "Passwords don't match.", False),
        ("123456789", "123456789", "", True),
    ],
)
def test_validate_password(
    monkeypatch: pytest.MonkeyPatch, password, confirm_password, expected_message, expected
):
    init_gui(monkeypatch)
    assert callbacks.validate_password(password, confirm_password) == expected
    if expected_message:
        assert get_error_message() == expected_message
