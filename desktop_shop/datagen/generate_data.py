# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:29:44 2020

Call using parent level database.py using:

    database generate

or:
    database generate --fast

@author: Korean_Crimson
"""
import logging
import random
import sqlite3
from typing import List, Protocol, Set

from desktop_shop import crypto, util
from desktop_shop.database import database
from desktop_shop.datagen import data

# combined with every salt for extra security in pw hashing
PEPPER = "secret"


class TableDataGenerator(Protocol):  # pylint: disable=missing-class-docstring
    def create_table(self, cursor):  # pylint: disable=missing-function-docstring
        """Creates the DB table"""

    def populate_table(self, cursor, amount: int):  # pylint: disable=missing-function-docstring
        """Populates the DB table"""


# pylint: disable=too-few-public-methods
class UserDataGenerator:
    """Used to generate data to fill the users table in the database"""

    def __init__(self, hash_iterations: int = 100_000):
        self.hash_iterations = hash_iterations
        self._email_cache: Set[str] = set()

    def create_table(self, cursor):
        """Creates the user table"""
        database.create_user_table(cursor)

    def populate_table(self, cursor, amount=10_000):
        """Populates the user table in the database (needs to already exist) with the
        amount of users specified in the input arg. Expects a database connection
        object to be passed in as first arg
        """
        first_names = data.fetch_first_names()
        last_names = data.fetch_last_names()

        for _ in range(amount):
            user_data = self._generate_random_user_data(first_names, last_names)
            password = self._generate_new_password()
            database.add_user(cursor, user_data, password, PEPPER, iterations=self.hash_iterations)

    def _generate_random_user_data(self, first_names, last_names):
        first_name = random.choice(list(first_names.keys()))
        last_name = random.choice(last_names)
        gender = first_names[first_name]
        join_date = data.get_random_date(start=(2014, 6, 1), end=(2020, 11, 1))
        dob = data.get_random_date(start=(1920, 1, 1), end=(2004, 6, 1))
        email_address = self._generate_random_email_address(first_name, last_name, dob)
        return [first_name, last_name, gender, dob, email_address, join_date]

    def _generate_random_email_address(self, first_name, last_name, dob):
        """generates unique email using _email_cache storing all generated emails"""
        email_address = ""
        domains = [
            "emailook.com",
            "oldlurk.com",
            "failmailprovider.co.uk",
            "beardgamemail.com",
        ]
        concatenators = ["-", "_", ".", "", ""]
        while not email_address or email_address in self._email_cache:
            domain = random.choice(domains)
            year, *_ = dob.split("-")
            random_string = "".join(
                [chr(random.randint(65, 90)) for _ in range(random.randint(1, 5))]
            )
            random_num = str(random.randint(0, 999))
            user = random.choices(
                [first_name, last_name, year, random_string, random_num],
                k=random.randint(2, 4),
            )
            concatenator = random.choice(concatenators)
            email_address = f"{concatenator.join(user)}@{domain}"
        self._email_cache.add(email_address)
        return email_address

    @staticmethod
    def _generate_new_password():
        return "password"


class ProductDataGenerator:
    """Used to generate data to fill the products table in the database"""

    def create_table(self, cursor):
        """Creates the products table"""
        database.create_products_table(cursor)

    def populate_table(self, cursor, amount=20):
        """Populates the products table in the database (needs to already exist)
        with the amount of products specified in the input arg. Expects a
        database connection to be passed in as first arg
        """
        for _ in range(amount):
            product_data = self._generate_random_product_data()
            database.add_product(cursor, product_data)

    @staticmethod
    def _generate_random_product_data():
        product_names = ["PumaVoxel", "PetaBit", "PersePhone"]
        series = ["A", "M", "S", "X", "Y", "Z"]
        versions = ["99", "10", "2", "33", "21"]

        name = random.choice(product_names)
        series_ = random.choice(series)
        version = random.choice(versions)
        product_name = f"{name} {series_}{version}"
        product_price = random.randint(10, 50) * 10 - 0.01  # Between 99.99 and 499.99

        product_data = [product_name, product_price]
        return product_data


class TransactionDataGenerator:
    """Used to generate data to fill the transactions table in the database"""

    def create_table(self, cursor):
        """Creates the transactions table"""
        database.create_detailed_transactions_table(cursor)
        database.create_transactions_table(cursor)

    @classmethod
    def populate_table(cls, cursor, amount=100_000):
        """Populates the transactions table in the database (needs to already exist)
        with the amount of transactions specified in the input arg. Expects a
        database connection object to be passed in as first arg
        """
        user_ids = database.query_user_ids_from_user_table(cursor)
        product_ids = database.query_product_ids_from_product_table(cursor)

        transactions = [cls._generate_random_transaction_data(user_ids) for _ in range(amount)]
        product_ids = [cls._generate_random_chosen_product_ids(product_ids) for _ in range(amount)]
        database.add_transactions(cursor, transactions, product_ids)

    @staticmethod
    def _generate_random_transaction_data(user_ids):
        user_id = random.choice(user_ids)
        date = data.get_random_date(start=(2004, 6, 1), end=(2020, 11, 1))

        transaction_data = [user_id, date]
        return transaction_data

    @staticmethod
    def _generate_random_chosen_product_ids(product_ids):
        number_of_products = random.randint(1, 5)
        chosen_product_ids = random.choices(product_ids, k=number_of_products)
        return list(map(str, chosen_product_ids))


class SessionDataGenerator:
    """Used to generate data to fill the sessions table in the database"""

    def create_table(self, cursor):
        """Creates the sessions table"""
        database.create_sessions_table(cursor)

    @staticmethod
    def populate_table(cursor, amount=25):
        """Populates the sessions table in the database (needs to already exist)
        with the amount of sessions specified in the input arg. Expects a
        database connection object to be passed in as first arg
        """
        user_ids = database.query_user_ids_from_user_table(cursor)
        chosen_user_ids = random.sample(user_ids, min(amount, len(user_ids)))

        for user_id in chosen_user_ids:
            session_id = crypto.generate_new_session_id()
            timestamp = util.generate_timestamp()
            session_data = [session_id, user_id, timestamp]
            database.add_session(cursor, session_data)


def generate(  # pylint: disable=too-many-arguments
    database_name: str,
    hash_iterations=100_000,
    transactions=100_000,
    users=10_000,
    products=20,
    sessions=25,
):
    """Generates the database, including user, products, transactions,
    detailed_transactions and sessions tables.
    The tables are pre-populated with random data of the specified sizes.
    """
    generators: List[TableDataGenerator] = [
        UserDataGenerator(hash_iterations),
        ProductDataGenerator(),
        TransactionDataGenerator(),
        SessionDataGenerator(),
    ]
    amounts = [users, products, transactions, sessions]
    with sqlite3.connect(database_name) as cursor:
        for amount, generator in zip(amounts, generators):
            generator.create_table(cursor)
            logging.info("Populating")
            generator.populate_table(cursor, amount)
            logging.info("Finished populating")
