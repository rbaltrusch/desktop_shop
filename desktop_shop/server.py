# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:07:42 2020

@author: Korean_Crimson
"""
from dataclasses import dataclass
import hmac
from typing import Any, Callable, Iterable, List, Optional, Tuple, TypeVar, Union
from desktop_shop import crypto, util
from desktop_shop.database import database
from desktop_shop.database.database import Connection
from desktop_shop.user import UserData

# pylint: disable=unused-argument
# pylint: disable=line-too-long
from desktop_shop.database.database import DuplicateUserError  # pylint: disable=unused-import

# combined with every salt for extra security in pw hashing
PEPPER = "secret"

_UserData = Union[UserData, List[str]]
_ProductData = List[Any]
T = TypeVar("T")
SessionId = str


class ServerSideLogInDataError(Exception):
    """Exception for login failures"""

    def __init__(self):
        super().__init__("Login data invalid. Corrupted login data was retrieved from the server.")


@dataclass
class Session:
    """Data to verify if a session is valid."""

    id: str
    user_email: str


def verify_database_call(
    function: Callable[..., T]
) -> Callable[..., Tuple[Optional[SessionId], Optional[T]]]:
    """Function decorator for database requests that work on sensitive data.
    This decorator mandates sending all the normal arguments, as well as two
    special keyword arguments (your linter may not like this), session_id and
    user_email. If the specified session_id cannot be found in the sessions table
    for the user identified by the user_email, the database request is denied.
    """

    def wrapper(cursor: Connection, *args, **kwargs) -> Tuple[Optional[SessionId], Optional[T]]:
        session: Session = kwargs.get("session")  # type: ignore
        verified = database.verify_session_id_by_user_email(cursor, session.id, session.user_email)
        if not verified:
            return None, None

        results = function(cursor, *args, **kwargs)

        # get new session id and add it to database
        new_session_id = _add_new_session(cursor, session.user_email)
        return new_session_id, results

    return wrapper


@verify_database_call
def query_user_data(cursor: Connection, user_email: str, *, session: Session) -> List[str]:
    """Queries the user data for the specified user_email from the users table."""
    return database.query_user_data_by_user_email(cursor, user_email)  # type: ignore


@verify_database_call
def add_transaction(  # type: ignore
    cursor: Connection, user_email: str, chosen_product_ids: Iterable[str], *, session: Session
) -> SessionId:  # type: ignore
    """Adds a new transaction containing the passed product ids for specified user."""
    user_id = database.query_user_id_from_user_email(cursor, user_email)
    date = util.get_current_date()
    transaction_data = [user_id, date]
    database.add_transaction(cursor, transaction_data, tuple(chosen_product_ids))


@verify_database_call
def update_user(cursor: Connection, user_data: _UserData, user_email: str, *, session: Session) -> SessionId:  # type: ignore
    """Updates the user data with the passed data"""
    database.update_user_by_user_email(cursor, list(user_data), user_email)


@verify_database_call
def update_user_password(cursor: Connection, password: str, user_email: str, *, session: Session) -> SessionId:  # type: ignore
    """Updates the user password with the passed data."""
    database.update_user_password(cursor, password, user_email, PEPPER)


def query_product_data_from_product_table(cursor: Connection) -> _ProductData:
    """Queries all product data from products table"""
    return database.query_product_data_from_product_table(cursor)


def query_product_data_from_product_table_by_product_ids(
    cursor: Connection, product_ids: Iterable[str]
) -> List[_ProductData]:
    """Queries product data from the products table by ids"""
    return database.query_product_data_from_product_table_by_product_ids(
        cursor, tuple(product_ids)
    )


def add_user(cursor: Connection, user_data: UserData, password: str) -> SessionId:
    """Adds a new user to the users table, with the user_data specified.
    Raises a DuplicateUserError if the specified email has already been used."""
    database.add_user(cursor, list(user_data), password, PEPPER)
    new_session_id = _add_new_session(cursor, user_data.email)
    return new_session_id


def login(cursor: Connection, user_email: str, password: str) -> Optional[SessionId]:
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
        if hmac.compare_digest(hashed_password, pw_hash):  # prevent timing attacks
            new_session_id = _add_new_session(cursor, user_email)
            return new_session_id
    return None


def _add_new_session(cursor: Connection, user_email: str) -> str:
    new_session_id = crypto.generate_new_session_id()
    timestamp = util.generate_timestamp()
    user_id = database.query_user_id_from_user_email(cursor, user_email)
    session_data = [new_session_id, user_id, timestamp]
    database.add_session(cursor, session_data)
    return new_session_id
