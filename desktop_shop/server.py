# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:07:42 2020

@author: Korean_Crimson
"""
import hmac

from desktop_shop import crypto, database, util

# combined with every salt for extra security in pw hashing
PEPPER = "secret"


class ServerSideLogInDataError(Exception):
    """Exception for login failures"""

    def __init__(self):
        super().__init__("Login data invalid. Corrupted login data was retrieved from the server.")


def verify_database_call(function):
    """Function decorator for database requests that work on sensitive data.
    This decorator mandates sending all the normal arguments, as well as two
    special keyword arguments (your linter may not like this), session_id and
    user_email. If the specified session_id cannot be found in the sessions table
    for the user identified by the user_email, the database request is denied.
    """

    def wrapper(*args, user_email="", session_id=""):
        cursor, *_ = args
        verified = database.verify_session_id_by_user_email(cursor, session_id, user_email)
        if verified:
            results = function(*args)

            # get new session id and add it to database
            new_session_id = _add_new_session(cursor, user_email)
        else:
            new_session_id = None
            results = None
        return new_session_id, results

    return wrapper


@verify_database_call
def query_user_data(cursor, user_email):
    """Queries the user data for the specified user_email from the users table.

    As this is a verified database call, a valid session id needs to be passed
    in (see decorator def) in order for the database request to succeed.
    """
    return database.query_user_data_by_user_email(cursor, user_email)


@verify_database_call
def add_transaction(cursor, user_email, chosen_product_ids):
    """Adds a new transaction containing the passed product ids for specified user.

    As this is a verified database call, a valid session id needs to be passed
    in (see decorator def) in order for the database request to succeed.
    """
    user_id = database.query_user_id_from_user_email(cursor, user_email)
    date = util.get_current_date()
    transaction_data = [user_id, date]
    return database.add_transaction(cursor, transaction_data, chosen_product_ids)


@verify_database_call
def update_user(cursor, user_data, user_email):
    """Updates the user data with the passed data

    As this is a verified database call, a valid session id needs to be passed
    in (see decorator def) in order for the database request to succeed.
    """
    return database.update_user_by_user_email(cursor, list(user_data), user_email)


@verify_database_call
def update_user_password(cursor, password, user_email):
    """Updates the user password with the passed data.

    As this is a verified database call, a valid session id needs to be passed
    in (see decorator def) in order for the database request to succeed.
    """
    return database.update_user_password(cursor, password, user_email, PEPPER)


def query_product_data_from_product_table(cursor):
    """Queries all product data from products table"""
    return database.query_product_data_from_product_table(cursor)


def query_product_data_from_product_table_by_product_ids(cursor, product_ids):
    """Queries product data from the products table by ids"""
    return database.query_product_data_from_product_table_by_product_ids(cursor, product_ids)


def add_user(cursor, user_data, password):
    """Adds a new user to the users table, with the user_data specified"""
    database.add_user(cursor, list(user_data), password, PEPPER)
    new_session_id = _add_new_session(cursor, user_data.email)
    return new_session_id


def login(cursor, user_email, password):
    """Gets the pw salt and pw hash from the database for the specified user.
    If they match the user_email and password passed into the login function,
    a new session id is generated, stored in the sessions table and returned.
    """
    data = database.query_pw_hash_and_salt_by_user_email(cursor, user_email)
    if len(data) == 3:
        # pylint: disable=unbalanced-tuple-unpacking
        pw_salt, pw_hash, hash_function_name = data
        hash_function = crypto.get_hash_function_from_string(hash_function_name)
        if hash_function is None:
            raise ServerSideLogInDataError

        hashed_password = hash_function.hash(password, pw_salt + PEPPER)
        if hmac.compare_digest(hashed_password, pw_hash):
            new_session_id = _add_new_session(cursor, user_email)
            return new_session_id
    return None


def _add_new_session(cursor, user_email):
    new_session_id = crypto.generate_new_session_id()
    timestamp = util.generate_timestamp()
    user_id = database.query_user_id_from_user_email(cursor, user_email)
    session_data = [new_session_id, user_id, timestamp]
    database.add_session(cursor, session_data)
    return new_session_id
