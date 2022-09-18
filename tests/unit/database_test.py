# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 18:57:51 2021

@author: richa
"""

# pylint: disable=missing-function-docstring
import functools
import sqlite3
from typing import List

import pytest

from desktop_shop import crypto, database
from desktop_shop.user import UserSignUpData

# in memory database to avoid errors when removing database file between tests
TEST_DB = "file:cachedb?mode=memory&cache=shared"
PASSWORD = "password123"
PEPPER = "2"
ITERATIONS = 100_000

user_data_fixture = [
    UserSignUpData("fi", "la", "m", "2000-01-01", "a@b.c", "2016-02-05"),
    UserSignUpData("fir", "las", "f", "2000-01-02", "test@email.c", "2016-02-05"),
]


def _mock_crypto(monkeypatch):
    class MockHashFunction:  # pylint: disable=missing-class-docstring
        def __init__(self, iterations: int) -> None:
            self.iterations = iterations

        def hash(self, password: str, salt: str) -> str:
            return password + salt

        def __str__(self):
            return "hashfn" + str(self.iterations)

    monkeypatch.setattr(crypto, "get_hash_function", MockHashFunction)
    generator = functools.partial(next, (str(x) for x in range(2, 10)))
    monkeypatch.setattr(crypto, "generate_new_salt", generator)


def _add_users(cursor, users: List[UserSignUpData]):
    database.create_user_table(cursor)
    for user in users:
        database.add_user(cursor, user, password=PASSWORD, pepper=PEPPER, iterations=ITERATIONS)


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, user_email, expected",
    [
        ([], "test@email.c", None),
        (user_data_fixture, "test@email.c", 2),
    ],
)
def test_query_user_id_from_user_email(users, user_email, expected):
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        assert database.query_user_id_from_user_email(cursor, user_email) == expected


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, expected",
    [
        ([], []),
        (user_data_fixture, [1, 2]),
    ],
)
def test_query_user_ids_from_user_table(users, expected):
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        assert database.query_user_ids_from_user_table(cursor) == expected


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, user_email, expected",
    [([], "test@email.c", []), (user_data_fixture, "test@email.c", list(user_data_fixture[1]))],
)
def test_query_user_data_by_user_email(users, user_email, expected):
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        assert database.query_user_data_by_user_email(cursor, user_email) == expected


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, user_id, expected",
    [
        ([], 1, []),
        (user_data_fixture, 1, list(user_data_fixture[0])),
        (user_data_fixture, 2, list(user_data_fixture[1])),
    ],
)
def test_query_user_data(users, user_id, expected):
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        assert database.query_user_data(cursor, user_id) == expected


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, user_email, expected",
    [
        ([], "a@b.c", []),
        (user_data_fixture, "a2@b.c", []),
        (
            user_data_fixture,
            "test@email.c",
            ["3", PASSWORD + "3" + PEPPER, "hashfn" + str(ITERATIONS)],
        ),
    ],
)
def test_query_pw_hash_and_salt_by_user_email(monkeypatch, users, user_email, expected):
    _mock_crypto(monkeypatch)
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        assert database.query_pw_hash_and_salt_by_user_email(cursor, user_email) == expected


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, user_data, user_id",
    [
        ([], list(user_data_fixture[0]), 1),
        (user_data_fixture, list(user_data_fixture[0]), 1),
    ],
)
def test_update_user(users, user_data, user_id):
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        database.update_user(cursor, user_data[:-1], user_id)
        if not users:
            return
        assert database.query_user_data(cursor, user_id) == user_data


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, user_data, user_email",
    [
        ([], list(user_data_fixture[0]), "a@b.c"),
        (user_data_fixture, list(user_data_fixture[0]), "a@b.c"),
    ],
)
def test_update_user_by_user_email(users, user_data, user_email):
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        database.update_user_by_user_email(cursor, user_data[:-1], user_email)
        if not users:
            return
        assert database.query_user_data_by_user_email(cursor, user_email) == user_data


@pytest.mark.slow
@pytest.mark.parametrize(
    "users, password, user_email, pepper, iterations, expected",
    [
        ([], "p123", "a@b.c", "pepp", ITERATIONS, ""),
        (user_data_fixture, "p123", "a@b.c", "pepp", ITERATIONS, "p123" + "2" + "pepp"),
    ],
)
def test_update_user_password(
    monkeypatch, users, password, user_email, pepper, iterations, expected
):
    _mock_crypto(monkeypatch)
    with sqlite3.connect(TEST_DB) as cursor:
        _add_users(cursor, users)
        _mock_crypto(monkeypatch)
        database.update_user_password(cursor, password, user_email, pepper, iterations)
        if not users:
            return
        assert database.query_pw_hash_and_salt_by_user_email(cursor, user_email)[1] == expected
