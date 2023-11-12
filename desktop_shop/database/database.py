# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:31:48 2020

@author: Korean_Crimson
"""

import argparse
from typing import Any, List

from desktop_shop import crypto
from desktop_shop.database import _statements


def query_user_id_from_user_email(cursor, user_email):
    """Queries for the user id of the user specified by the user_email passed (unique)"""
    command = _statements.QUERY_USER_ID_BY_EMAIL
    user_ids = [user_id for user_id, *_ in cursor.execute(command, [user_email])]
    return user_ids[0] if user_ids else None


def query_user_ids_from_user_table(cursor):
    """Returns all user_ids found in users table as a list"""
    user_ids = [user_id for user_id, *_ in cursor.execute(_statements.QUERY_USER_IDS)]
    return user_ids


def query_product_ids_from_product_table(cursor):
    """Returns all product ids found in products table as a list"""
    product_ids = [prod_id for prod_id, *_ in cursor.execute(_statements.QUERY_PRODUCT_IDS)]
    return product_ids


def query_product_data_from_product_table(cursor):
    """Queries all produt data from the products table"""
    data = [list(row) for row in cursor.execute(_statements.QUERY_PRODUCTS)]
    return data


def query_product_data_from_product_table_by_product_ids(cursor, product_ids: List[str]):
    """Queries product data from the products table, by the passed product ids"""

    # sanitize input and make sure all product ids are only numeric
    if not all(product_id.isnumeric() for product_id in product_ids):
        return []

    joined_product_ids = f"({','.join(map(str, product_ids))})"

    # This .format looks like an SQL injection vulnerability, but there is currently
    # no other way to execute Sqlite "WHERE something IN list" statements in Python.
    # As we make sure the passed list only contains numeric strings, this should be OK.
    command = "SELECT * FROM products WHERE product_id IN " + joined_product_ids
    data = [list(row) for row in cursor.execute(command)]
    return data


def query_product_price_from_product_table(cursor, product_ids):
    """Returns all prices found for the specified product ids as a list"""

    # sanitize input and make sure all product ids are only numeric
    if not all(product_id.isnumeric() for product_id in product_ids):
        return []

    joined_product_ids = f"({','.join(map(str, product_ids))})"
    command = "SELECT price FROM products WHERE product_id IN " + joined_product_ids
    product_prices = [product_price for product_price, *_ in cursor.execute(command)]
    return product_prices


def query_user_data_by_user_email(cursor, user_email):
    """Queries the user data from the users table, by the user identified by the user_email"""
    command = _statements.QUERY_USER_BY_EMAIL
    data = list(cursor.execute(command, [user_email]))
    return list(data[0]) if data else []


def query_user_data(cursor, user_id):
    """Queries the data for the user from the users table, by the user id passed"""
    command = _statements.QUERY_USER_BY_ID
    data = list(cursor.execute(command, [str(user_id)]))
    return list(data[0]) if data else []


def query_pw_hash_and_salt_by_user_email(cursor, user_email):
    """Queries the password hash, salt and hashing function from the users table
    for the specified user_email
    """
    command = _statements.QUERY_USER_PW_HASH_AND_SALT_BY_EMAIL
    data = list(cursor.execute(command, [user_email]))
    return list(data[0]) if data else []


def _get_last_inserted_id(cursor):
    """Returns the id of the transaction last added to the transactions table"""
    transaction_id, *_ = [id_ for id_, *_ in cursor.execute(_statements.QUERY_LAST_INSERTED_ID)]
    return transaction_id


def verify_session_id(cursor, session_id: str, user_id: int):
    """Verifies that the passed session_id is held by a user identified by the passed user id"""
    command = _statements.QUERY_SESSION_BY_ID_AND_USER
    data = cursor.execute(command, [session_id, user_id])
    data = [d for d, *_ in data]
    verified = bool(data and data[0] == session_id)
    return verified


def verify_session_id_by_user_email(cursor, session_id: str, user_email: int):
    """Verifies that the passed session_id is held by a user identified by the passed user_email"""
    command = _statements.QUERY_SESSION_BY_ID_AND_EMAIL
    data = cursor.execute(command, [session_id, user_email])
    data = [d for d, *_ in data]
    verified = bool(data and data[0] == session_id)
    return verified


def add_user(cursor, user_data, password, pepper="", iterations=100_000):
    """Adds a user with the specified user data to the users table"""
    # hash password
    salt = crypto.generate_new_salt()
    hash_function = crypto.get_hash_function(iterations)
    hashed_password = hash_function.hash(password, salt + pepper)
    user_data = list(user_data) + [salt, hashed_password, str(hash_function)]

    cursor.execute(_statements.INSERT_USER, user_data)


def update_user(cursor, user_data, user_id):
    """user_data needs to be a full set of user_data, without the user_id,
    which is passed separately
    """
    user_data.append(user_id)
    cursor.execute(_statements.UPDATE_USER_BY_ID, user_data)


def update_user_password(cursor, password, user_email, pepper="", iterations=100_000):
    """Updates the password hash in the users table for the user specified"""
    salt = crypto.generate_new_salt()
    pw_hash = crypto.get_hash_function(iterations).hash(password, salt + pepper)
    command = _statements.UPDATE_USER_PW_BY_EMAIL
    cursor.execute(command, [pw_hash, salt, user_email])


def update_user_by_user_email(cursor, user_data, user_email):
    """user_data needs to be a full set of user_data, without the user_id,
    which is passed separately
    """
    user_data.append(user_email)
    cursor.execute(_statements.UPDATE_USER_BY_EMAIL, user_data)


def add_transaction(cursor, transaction_data: List[Any], chosen_product_ids: List[str]):
    """adds a transaction with the specified transaction data to the transactions
    table and the detailed transactions table.
    """
    product_prices = query_product_price_from_product_table(cursor, chosen_product_ids)
    cost = sum(product_prices)
    transaction_data.append(cost)
    cursor.execute(_statements.INSERT_TRANSACTION, transaction_data)

    transaction_id = _get_last_inserted_id(cursor)
    for chosen_product_id in chosen_product_ids:
        cursor.execute(
            _statements.INSERT_DETAILED_TRANSACTION, [transaction_id, chosen_product_id]
        )


def add_transactions(
    cursor, transaction_datas: List[List[Any]], chosen_product_ids: List[List[str]]
):
    """Adds all specified transactions"""
    product_data = {
        str(id_): price for id_, _, price in query_product_data_from_product_table(cursor)
    }
    for transaction_data, chosen_product_ids_ in zip(transaction_datas, chosen_product_ids):
        cost = sum(product_data[i] for i in chosen_product_ids_)
        transaction_data.append(cost)

    # note: cannot use cursor.executemany because we need the id of the inserted transaction
    # after each insert.
    for transaction_data, chosen_product_ids_ in zip(transaction_datas, chosen_product_ids):
        cursor.execute(_statements.INSERT_TRANSACTION, transaction_data)

        transaction_id = _get_last_inserted_id(cursor)
        for chosen_product_id in chosen_product_ids_:
            cursor.execute(
                _statements.INSERT_DETAILED_TRANSACTION, [transaction_id, chosen_product_id]
            )


def add_session(cursor, session_data):
    """adds a session with the specified session data to the session table"""
    cursor.execute(_statements.INSERT_SESSION, session_data)


def add_product(cursor, product_data):
    """adds a product with the specified product data to the products table"""
    cursor.execute(_statements.INSERT_PRODUCT, product_data)


def create_user_table(cursor):
    """Creates user table. Only called in generate_database"""
    cursor.executescript(_statements.CREATE_OR_REPLACE_USERS_TABLE)


def create_transactions_table(cursor):
    """Creates transactions table. Only called in generate_database"""
    cursor.executescript(_statements.CREATE_OR_REPLACE_TRANSACTIONS_TABLE)


def create_detailed_transactions_table(cursor):
    """Creates detailed transactions table. Only called in generate_database"""
    cursor.executescript(_statements.CREATE_OR_REPLACE_DETAILED_TRANSACTIONS_TABLE)


def create_products_table(cursor):
    """Creates products table. Only called in generate_database"""
    cursor.executescript(_statements.CREATE_OR_REPLACE_PRODUCTS_TABLE)


def create_sessions_table(cursor):
    """Creates sessions table. Only called in generate_database"""
    cursor.executescript(_statements.CREATE_OR_REPLACE_SESSIONS_TABLE)


def generate_database():
    """Generates a fresh database with the provided cli args"""
    from desktop_shop.datagen import generate_data  # pylint: disable=import-outside-toplevel

    parser = argparse.ArgumentParser(description="Database generation interface")
    parser.add_argument("action", choices=["generate"], help="database action to be performed")
    parser.add_argument("--name", default="main.db", help="The name of the database")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="reduces number of password hashing operations",
    )
    parser.add_argument("--minimal", action="store_true", help="reduces size of all tables to 1")
    parser.add_argument(
        "--transactions",
        default=100_000,
        type=int,
        help="pass number of transactions to be added to database",
    )
    parser.add_argument(
        "--users",
        default=10_000,
        type=int,
        help="pass number of users to be added to database",
    )
    parser.add_argument(
        "--products",
        default=20,
        type=int,
        help="pass number of products to be added to database",
    )
    args = parser.parse_args()

    if args.action == "generate":
        number_of_hashes = 1 if args.fast else 100_000  # pylint: disable=invalid-name
        transactions, users, products = (
            (1, 1, 1) if args.minimal else (args.transactions, args.users, args.products)
        )
        generate_data.generate(
            args.name, number_of_hashes, transactions=transactions, users=users, products=products
        )


if __name__ == "__main__":
    generate_database()
