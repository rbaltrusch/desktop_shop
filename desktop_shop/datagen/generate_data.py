# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:29:44 2020

Call using parent level database.py using:

    database generate

or:
    database generate --fast

@author: Korean_Crimson
"""
import random
import sqlite3

from desktop_shop import crypto, database, util
from desktop_shop.datagen import data

# combined with every salt for extra security in pw hashing
PEPPER = "secret"


# pylint: disable=too-few-public-methods
class UserDataGenerator:
    """Used to generate data to fill the users table in main.db"""

    def __init__(self):
        self._email_cache = []

    def populate_user_table(self, cursor, number_of_users=10_000, hash_iterations=100_000):
        """Populates the user table in main.db (needs to already exist) with the
        amount of users specified in the input arg. Expects a database connection
        object to be passed in as first arg
        """
        first_names = data.fetch_first_names()
        last_names = data.fetch_last_names()

        for _ in range(number_of_users):
            user_data = self._generate_random_user_data(first_names, last_names)
            password = self._generate_new_password()
            database.add_user(cursor, user_data, password, PEPPER, iterations=hash_iterations)

    def _generate_random_user_data(self, first_names, last_names):
        first_name = random.choice(list(first_names.keys()))
        last_name = random.choice(last_names)
        gender = first_names[first_name]
        join_date = data.get_random_date(start=[2014, 6, 1], end=[2020, 11, 1])
        dob = data.get_random_date(start=[1920, 1, 1], end=[2004, 6, 1])
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
        self._email_cache.append(email_address)
        return email_address

    @staticmethod
    def _generate_new_password():
        return "password"


class ProductDataGenerator:
    """Used to generate data to fill the products table in main.db"""

    def populate_products_table(self, cursor, number_of_products=20):
        """Populates the products table in main.db (needs to already exist)
        with the amount of products specified in the input arg. Expects a
        database connection to be passed in as first arg
        """
        for _ in range(number_of_products):
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
    """Used to generate data to fill the transactions table in main.db"""

    @classmethod
    def populate_transactions_table(cls, cursor, number_of_transactions=100_000):
        """Populates the transactions table in main.db (needs to already exist)
        with the amount of transactions specified in the input arg. Expects a
        database connection object to be passed in as first arg
        """
        user_ids = database.query_user_ids_from_user_table(cursor)
        product_ids = database.query_product_ids_from_product_table(cursor)

        for _ in range(number_of_transactions):
            chosen_product_ids = cls._generate_random_chosen_product_ids(product_ids)
            transaction_data = cls._generate_random_transaction_data(user_ids)
            database.add_transaction(cursor, transaction_data, chosen_product_ids)

    @staticmethod
    def _generate_random_transaction_data(user_ids):
        user_id = random.choice(user_ids)
        date = data.get_random_date(start=[2004, 6, 1], end=[2020, 11, 1])

        transaction_data = [user_id, date]
        return transaction_data

    @staticmethod
    def _generate_random_chosen_product_ids(product_ids):
        number_of_products = random.randint(1, 5)
        chosen_product_ids = random.choices(product_ids, k=number_of_products)
        return list(map(str, chosen_product_ids))


class SessionDataGenerator:
    """Used to generate data to fill the sessions table in main.db"""

    @staticmethod
    def populate_sessions_table(cursor, number_of_sessions=25):
        """Populates the sessions table in main.db (needs to already exist)
        with the amount of sessions specified in the input arg. Expects a
        database connection object to be passed in as first arg
        """
        user_ids = database.query_user_ids_from_user_table(cursor)
        chosen_user_ids = random.sample(user_ids, min(number_of_sessions, len(user_ids)))

        for user_id in chosen_user_ids:
            session_id = crypto.generate_new_session_id()
            timestamp = util.generate_timestamp()
            session_data = [session_id, user_id, timestamp]
            database.add_session(cursor, session_data)


def generate(hash_iterations=100_000, transactions=100_000, users=10_000, products=20):
    """Generates the database, including user, products, transactions,
    detailed_transactions and sessions tables.
    The tables are pre-populated with random data of the specified sizes.
    """

    with sqlite3.connect("main.db") as cursor:
        # create and populate user table
        database.create_user_table(cursor)
        UserDataGenerator().populate_user_table(
            cursor, hash_iterations=hash_iterations, number_of_users=users
        )

        # create and populate products table
        database.create_products_table(cursor)
        ProductDataGenerator().populate_products_table(cursor, number_of_products=products)

        # create detailed transactions table
        database.create_detailed_transactions_table(cursor)

        # create and populate transactions table
        database.create_transactions_table(cursor)
        TransactionDataGenerator.populate_transactions_table(
            cursor, number_of_transactions=transactions
        )

        # create and populate sessions table
        database.create_sessions_table(cursor)
        SessionDataGenerator.populate_sessions_table(cursor)


if __name__ == "__main__":
    generate()
