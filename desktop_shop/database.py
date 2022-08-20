# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:31:48 2020

@author: Korean_Crimson
"""
from desktop_shop import crypto


def query_user_id_from_user_email(cursor, user_email):
    """Queries for the user id of the user specified by the user_email passed (unique)"""
    command = "SELECT user_id FROM users WHERE email_address = ?"
    user_ids = [user_id for user_id, *_ in cursor.execute(command, [user_email])]
    return user_ids[0] if user_ids else None


def query_user_ids_from_user_table(cursor):
    """Returns all user_ids found in users table as a list"""
    user_ids = [user_id for user_id, *_ in cursor.execute("SELECT user_id FROM users")]
    return user_ids


def query_product_ids_from_product_table(cursor):
    """Returns all product ids found in products table as a list"""
    product_ids = [prod_id for prod_id, *_ in cursor.execute("SELECT product_id FROM products")]
    return product_ids


def query_product_data_from_product_table(cursor):
    """Queries all produt data from the products table"""
    data = [list(row) for row in cursor.execute("SELECT * FROM products")]
    return data


def query_product_data_from_product_table_by_product_ids(cursor, product_ids):
    """Queries product data from the products table, by the passed product ids"""

    # sanitize input and make sure all product ids are only numeric
    if not all(product_id.isnumeric() for product_id in product_ids):
        return []

    joined_product_ids = ",".join([str(product_id) for product_id in product_ids])
    joined_product_ids_str = f"({joined_product_ids})"

    # This .format looks like an SQL injection vulnerability, but there is currently
    # no other way to execute Sqlite "WHERE something IN list" statements in Python.
    # As we make sure the passed list only contains numeric strings, this should be OK.
    command = "SELECT * FROM products WHERE product_id IN " + joined_product_ids_str
    data = [list(row) for row in cursor.execute(command)]
    return data


def query_product_price_from_product_table(cursor, product_ids):
    """Returns all prices found for the specified product ids as a list"""

    # sanitize input and make sure all product ids are only numeric
    if not all(product_id.isnumeric() for product_id in product_ids):
        return []

    joined_product_ids = ",".join([str(product_id) for product_id in product_ids])
    joined_product_ids_str = f"({joined_product_ids})"

    command = "SELECT price FROM products WHERE product_id IN " + joined_product_ids_str
    product_prices = [product_price for product_price, *_ in cursor.execute(command)]
    return product_prices


def query_user_data_by_user_email(cursor, user_email):
    """Queries the user data from the users table, by the user identified by the user_email"""
    command = """SELECT
                    first_name,
                    last_name,
                    gender,
                    dob,
                    email_address,
                    join_date
                FROM users
                WHERE email_address = ?"""

    data = cursor.execute(command, [user_email])
    data = list(data)
    return list(data[0]) if data else []


def query_user_data(cursor, user_id):
    """Queries the data for the user from the users table, by the user id passed"""
    command = """'SELECT
                    first_name,
                    last_name,
                    gender,
                    dob,
                    email_address,
                    join_date,
                FROM users
                WHERE user_id = ?"""

    data = cursor.execute(command, [str(user_id)])
    data = list(data)
    return list(data[0]) if data else []


def query_pw_hash_and_salt_by_user_email(cursor, user_email):
    """Queries the password hash, salt and hashing function from the users table
    for the specified user_email
    """
    command = "SELECT pw_salt, pw_hash, hash_function FROM users WHERE email_address = ?"
    data = cursor.execute(command, [user_email])
    data = list(data)
    return list(data[0]) if data else []


def get_last_added_transaction_id_from_transactions_table(cursor):
    """Returns the id of the transaction last added to the transactions table"""
    transaction_id, *_ = [id_ for id_, *_ in cursor.execute("""SELECT last_insert_rowid()""")]
    return transaction_id


def verify_session_id(cursor, session_id, user_id):
    """Verifies that the passed session_id is held by a user identified by the passed user id"""
    command = """SELECT session_id
                FROM sessions
                WHERE session_id = ?
                AND user_id = ?"""

    data = cursor.execute(command, [session_id, user_id])
    data = [d for d, *_ in data]
    verified = data and data[0] == session_id

    # DONT REMOVE: for some reason, without this useless if, the function doesnt work....
    if not verified:
        verified = False
    return verified


def verify_session_id_by_user_email(cursor, session_id, user_email):
    """Verifies that the passed session_id is held by a user identified by the passed user_email"""
    command = """SELECT session_id FROM sessions
                  WHERE session_id = ?
                  AND user_id IN
                  (
                      SELECT user_id FROM users
                      WHERE email_address = ?)"""

    data = cursor.execute(command, [session_id, user_email])
    data = [d for d, *_ in data]
    verified = data and data[0] == session_id
    if not verified:
        verified = False
    return verified


def add_user(cursor, user_data, password, pepper="", iterations=100_000):
    """Adds a user with the specified user data to the users table"""
    command = """INSERT INTO users
                (first_name, last_name, gender, dob, email_address,
                join_date, pw_salt, pw_hash, hash_function)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    # hash password
    salt = crypto.generate_new_salt()
    hash_function = crypto.get_hash_function(iterations)
    hashed_password = hash_function.hash(password, salt + pepper)
    user_data = list(user_data) + [salt, hashed_password, str(hash_function)]

    cursor.execute(command, user_data)


def update_user(cursor, user_data, user_id):
    """user_data needs to be a full set of user_data, without the user_id,
    which is passed separately
    """
    user_data.append(user_id)
    command = """UPDATE users
                SET
                    first_name = ?,
                    last_name = ?,
                    gender = ?,
                    dob = ?,
                    email_address = ?
                WHERE user_id = ?"""
    cursor.execute(command, user_data)


def update_user_password(cursor, password, user_email, pepper="", iterations=100_000):
    """Updates the password hash in the users table for the user specified"""
    salt = crypto.generate_new_salt()
    pw_hash = crypto.get_hash_function(iterations).hash(password, salt + pepper)
    command = "UPDATE users SET pw_hash = ?, pw_salt = ? WHERE email_address = ?"
    cursor.execute(command, [pw_hash, salt, user_email])


def update_user_by_user_email(cursor, user_data, user_email):
    """user_data needs to be a full set of user_data, without the user_id,
    which is passed separately
    """
    user_data.append(user_email)
    command = """UPDATE users
                SET
                    first_name = ?,
                    last_name = ?,
                    gender = ?,
                    dob = ?,
                    email_address = ?
                WHERE email_address = ?"""
    cursor.execute(command, user_data)


def add_transaction(cursor, transaction_data, chosen_product_ids):
    """adds a transaction with the specified transaction data to the transactions
    table and the detailed transactions table.
    """
    product_prices = query_product_price_from_product_table(cursor, chosen_product_ids)
    cost = sum(product_prices)
    transaction_data.append(cost)

    command = "INSERT INTO transactions (user_id, date, cost) VALUES (?, ?, ?)"
    cursor.execute(command, transaction_data)

    transaction_id = get_last_added_transaction_id_from_transactions_table(cursor)

    command = "INSERT INTO detailed_transactions (transaction_id, product_id) VALUES (?, ?)"
    for chosen_product_id in chosen_product_ids:
        cursor.execute(command, [transaction_id, chosen_product_id])


def add_session(cursor, session_data):
    """adds a session with the specified session data to the session table"""
    command = "INSERT INTO sessions (session_id, user_id, timestamp) VALUES (?, ?, ?)"
    cursor.execute(command, session_data)


def add_product(cursor, product_data):
    """adds a product with the specified product data to the products table"""
    command = "INSERT INTO products (name, price) VALUES (?, ?)"
    cursor.execute(command, product_data)


def create_user_table(cursor):
    """Creates user table. Only called in generate_database"""
    # remove table
    cursor.execute("""DROP TABLE IF EXISTS users""")

    # create table
    cursor.execute(
        """CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    gender TEXT,
                    dob TEXT CHECK(CAST(strftime('%s', join_date)  AS  integer) >
                                   CAST(strftime('%s', dob)  AS  integer)),
                    email_address TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    join_date TEXT NOT NULL,
                    pw_salt NOT NULL,
                    pw_hash NOT NULL,
                    hash_function NOT NULL
                    CHECK (email_address LIKE '%_@_%._%')
                    )"""
    )

    # remove index based on user id
    cursor.execute("""DROP INDEX IF EXISTS idx_user_id""")

    # create index based on user_id
    cursor.execute("""CREATE INDEX idx_user_id ON users(user_id)""")


def create_transactions_table(cursor):
    """Creates transactions table. Only called in generate_database"""
    # remove table
    cursor.execute("""DROP TABLE IF EXISTS transactions""")

    # create table
    cursor.execute(
        """CREATE TABLE transactions (
                    transaction_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    date TEXT,
                    cost REAL NOT NULL,
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                    )"""
    )

    # drop index based on user_id
    cursor.execute("""DROP INDEX IF EXISTS idx_user_id""")

    # create index based on user_id
    cursor.execute("""CREATE INDEX idx_user_id ON transactions(user_id)""")


def create_detailed_transactions_table(cursor):
    """Creates detailed transactions table. Only called in generate_database"""
    # remove table
    cursor.execute("""DROP TABLE IF EXISTS detailed_transactions""")

    # create table
    cursor.execute(
        """CREATE TABLE detailed_transactions (
                    transaction_id INTEGER,
                    product_id INTEGER,
                    FOREIGN KEY (transaction_id)
                        REFERENCES transactions (transaction_id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT,
                    FOREIGN KEY (product_id)
                        REFERENCES products (product_id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT)
                    """
    )


def create_products_table(cursor):
    """Creates products table. Only called in generate_database"""
    # remove table
    cursor.execute("""DROP TABLE IF EXISTS products""")

    # create table
    cursor.execute(
        """CREATE TABLE products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT,
                    price REAL NOT NULL
                    )"""
    )


def create_sessions_table(cursor):
    """Creates sessions table. Only called in generate_database"""
    # remove table
    cursor.execute("""DROP TABLE IF EXISTS sessions""")

    # create table
    cursor.execute(
        """CREATE TABLE sessions(
                    session_id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    timestamp TEXT,
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                    )"""
    )


if __name__ == "__main__":
    import argparse

    from desktop_shop.datagen import generate_data

    parser = argparse.ArgumentParser(description="Database generation interface")
    parser.add_argument("action", choices=["generate"], help="database action to be performed")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="reduces number of password hashing operations",
    )
    parser.add_argument("--minimal", action="store_true", help="reduces size of all tables to 1")
    parser.add_argument(
        "--transactions",
        nargs=1,
        default=100_000,
        type=int,
        help="pass number of transactions to be added to database",
    )
    parser.add_argument(
        "--users",
        nargs=1,
        default=10_000,
        type=int,
        help="pass number of users to be added to database",
    )
    parser.add_argument(
        "--products",
        nargs=1,
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
            number_of_hashes, transactions=transactions, users=users, products=products
        )
