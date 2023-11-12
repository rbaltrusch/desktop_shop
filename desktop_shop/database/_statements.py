# -*- coding: utf-8 -*-
"""Contains all SQL statements"""

import os
import pathlib

SqlQuery = str


def load_statement(filepath: os.PathLike) -> SqlQuery:
    """Loads an SQL statement from the specified file"""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


_PATH = pathlib.Path(os.path.dirname(__file__), "sql")
QUERY_USER_ID_BY_EMAIL = load_statement(_PATH / "query_user_id_by_email.sql")
QUERY_USER_IDS = load_statement(_PATH / "query_user_ids.sql")
QUERY_PRODUCT_IDS = load_statement(_PATH / "query_product_ids.sql")
QUERY_PRODUCTS = load_statement(_PATH / "query_products.sql")
QUERY_USER_BY_EMAIL = load_statement(_PATH / "query_user_by_email.sql")
QUERY_USER_BY_ID = load_statement(_PATH / "query_user_by_id.sql")
QUERY_USER_PW_HASH_AND_SALT_BY_EMAIL = load_statement(
    _PATH / "query_user_pw_hash_and_salt_by_email.sql"
)
QUERY_LAST_INSERTED_ID = load_statement(_PATH / "query_last_inserted_id.sql")
QUERY_SESSION_BY_ID_AND_USER = load_statement(_PATH / "query_session_by_id_and_user.sql")
QUERY_SESSION_BY_ID_AND_EMAIL = load_statement(_PATH / "query_session_by_id_and_email.sql")


UPDATE_USER_BY_ID = load_statement(_PATH / "update_user_by_id.sql")
UPDATE_USER_PW_BY_EMAIL = load_statement(_PATH / "update_user_pw_by_email.sql")
UPDATE_USER_BY_EMAIL = load_statement(_PATH / "update_user_by_email.sql")

INSERT_USER = load_statement(_PATH / "insert_user.sql")
INSERT_TRANSACTION = load_statement(_PATH / "insert_transaction.sql")
INSERT_DETAILED_TRANSACTION = load_statement(_PATH / "insert_detailed_transaction.sql")
INSERT_SESSION = load_statement(_PATH / "insert_session.sql")
INSERT_PRODUCT = load_statement(_PATH / "insert_product.sql")

CREATE_OR_REPLACE_SESSIONS_TABLE = load_statement(_PATH / "create_or_replace_sessions_table.sql")
CREATE_OR_REPLACE_PRODUCTS_TABLE = load_statement(_PATH / "create_or_replace_products_table.sql")
CREATE_OR_REPLACE_TRANSACTIONS_TABLE = load_statement(
    _PATH / "create_or_replace_transactions_table.sql"
)
CREATE_OR_REPLACE_DETAILED_TRANSACTIONS_TABLE = load_statement(
    _PATH / "create_or_replace_detailed_transactions_table.sql"
)
CREATE_OR_REPLACE_USERS_TABLE = load_statement(_PATH / "create_or_replace_users_table.sql")
