# -*- coding: utf-8 -*-
"""Tests for the desktop_shop.datagen.generate_data module"""
import random
import string
import sys
from typing import Dict, List

import pytest

from desktop_shop import database
from desktop_shop.datagen import generate_data
from desktop_shop.datagen.data import DateTuple, get_random_date


class MockData:
    """Mock desktop_shop.datagen.data module"""

    @staticmethod
    def fetch_first_names() -> Dict[str, str]:
        """fetches first names from the web and returns them as a dict in the
        format first_name: gender
        """
        return {
            "".join(random.choices(string.ascii_lowercase, k=10)): random.choice(["m", "f"])
            for _ in range(1000)
        }

    @staticmethod
    def fetch_last_names() -> List[str]:
        """fetches last names from the web and returns them in a list"""
        return ["".join(random.choices(string.ascii_lowercase, k=10)) for _ in range(1000)]

    @staticmethod
    def get_random_date(start: DateTuple, end: DateTuple) -> str:
        """Returns a random data between start and end"""
        return get_random_date(start, end)


# pylint: disable=unused-argument, missing-function-docstring
class MockDatabase:
    """Mock desktop_shop.database module"""

    def __init__(self):
        self.users = []
        self.user_ids: List[str] = []
        self.sessions = []
        self.transactions = []
        self.detailed_transactions = []
        self.products = []
        self.product_ids: List[str] = []
        self.hash_iterations = []

    def create_user_table(self, cursor):
        self.users = []
        self.user_ids = []

    def create_products_table(self, cursor):
        self.products = []
        self.product_ids = []

    def create_detailed_transactions_table(self, cursor):
        self.detailed_transactions = []

    def create_transactions_table(self, cursor):
        self.transactions = []

    def create_sessions_table(self, cursor):
        self.sessions = []

    def add_user(self, cursor, user_data, password, pepper, iterations):
        self.user_ids.append(len(self.users))
        self.hash_iterations.append(iterations)
        self.users.append(user_data + [password, pepper, iterations])

    def add_product(self, cursor, product_data):
        self.product_ids.append(len(self.products))
        self.products.append(product_data)

    def add_transactions(self, cursor, transactions, product_ids):
        self.transactions.extend(transactions)
        existing_ids = set(map(str, self.product_ids))
        existing_user_ids = set(self.user_ids)
        assert all(all(id_ in existing_ids for id_ in ids) for ids in product_ids)
        assert all(user_id in existing_user_ids for user_id, _ in transactions)
        self.detailed_transactions.extend(product_ids)

    def add_session(self, cursor, session_data):
        _, user_id, _ = session_data
        assert user_id in self.user_ids
        self.sessions.append(session_data)

    def query_user_ids_from_user_table(self, cursor) -> List[str]:
        return self.user_ids

    def query_product_ids_from_product_table(self, cursor) -> List[str]:
        return self.product_ids


@pytest.mark.parametrize(
    "hash_iterations, transactions, users, products, sessions",
    [
        (1, 0, 0, 0, 0),
        (1, 1, 1, 1, 1),
        (1, 20, 5, 16, 9),
    ],
)
def test_generate(monkeypatch, hash_iterations, transactions, users, products, sessions):
    mock_database = MockDatabase()
    monkeypatch.setattr(generate_data, "database", mock_database)
    monkeypatch.setattr(generate_data, "data", MockData)
    generate_data.generate(
        database_name="test.db",
        hash_iterations=hash_iterations,
        transactions=transactions,
        users=users,
        products=products,
        sessions=sessions,
    )

    assert len(mock_database.transactions) == transactions
    assert (
        len(mock_database.detailed_transactions) >= transactions
    )  # at least one chosen product per transacion
    assert len(mock_database.users) == users
    assert len(mock_database.products) == products
    assert len(mock_database.sessions) == min(
        users, sessions
    )  # cannot have more sessions than users


@pytest.mark.parametrize(
    "args, transactions, users, products, hashes",
    [
        ("generate --transactions 2 --users 3 --products 4", 2, 3, 4, 100_000),
        ("generate --transactions 2 --users 3 --products 4 --fast", 2, 3, 4, 1),
        ("generate --minimal", 1, 1, 1, 100_000),
        ("generate --fast --minimal --name=test.db", 1, 1, 1, 1),
    ],
)
def test_generate_database(args, transactions, users, products, hashes, monkeypatch):
    mock_database = MockDatabase()
    monkeypatch.setattr(sys, "argv", sys.argv[0:1] + args.split(" "))
    monkeypatch.setattr(generate_data, "database", mock_database)
    monkeypatch.setattr(generate_data, "data", MockData)
    database.generate_database()

    sessions = 25
    assert len(mock_database.transactions) == transactions
    assert (
        len(mock_database.detailed_transactions) >= transactions
    )  # at least one chosen product per transacion
    assert len(mock_database.users) == users
    assert len(mock_database.products) == products
    assert len(mock_database.sessions) == min(users, sessions)
    assert all(h == hashes for h in mock_database.hash_iterations)
