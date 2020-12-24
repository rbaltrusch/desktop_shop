# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:31:48 2020

@author: Korean_Crimson
"""

import crypto

def query_user_id_from_user_email(cursor, user_email):
    command = 'SELECT user_id FROM users WHERE email_address = ?'
    user_ids = [user_id for user_id, *_ in cursor.execute(command, [user_email])]
    return user_ids[0] if user_ids else None

def query_user_ids_from_user_table(cursor):
    '''Returns all user_ids found in users table as a list'''
    user_ids = [user_id for user_id, *_ in cursor.execute('SELECT user_id FROM users')]
    return user_ids

def query_product_ids_from_product_table(cursor):
    '''Returns all product ids found in products table as a list'''
    product_ids = [product_id for product_id, *_ in cursor.execute('SELECT product_id FROM products''')]
    return product_ids

def query_product_price_from_product_table(cursor, product_ids):
    '''Returns all prices found for the specified product ids as a list'''
    joined_product_ids = ','.join([str(product_id) for product_id in product_ids])
    joined_product_ids_str = f"({joined_product_ids})"

    command = 'SELECT price FROM products WHERE product_id IN {}'.format(joined_product_ids_str)
    product_prices = [product_price for product_price, *_ in cursor.execute(command)] #joined_product_ids_str
    return product_prices

def query_user_data_by_user_email(cursor, user_email):
    data = cursor.execute('SELECT * FROM users where email_address = ?', [user_email])
    return list(list(data)[0])

def query_user_data(cursor, user_id):
    data = cursor.execute('SELECT * FROM users WHERE user_id = ?', [str(user_id)])
    return list(list(data)[0])

def query_pw_hash_and_salt_by_user_email(cursor, user_email):
    command = 'SELECT pw_salt, pw_hash FROM users WHERE email_address = ?'
    data = cursor.execute(command, [user_email])
    return list(list(data)[0])

def get_last_added_transaction_id_from_transactions_table(cursor):
    transaction_id, *_ = [id_ for id_, *_ in cursor.execute('''SELECT last_insert_rowid()''')]
    return transaction_id

def verify_session_id(cursor, session_id, user_id):
    data = cursor.execute('SELECT session_id FROM sessions WHERE session_id = ? AND user_id = ?', [session_id, user_id])
    data = [d for d, *_ in data]
    verified = data and data[0] == session_id
    if not verified:
        verified = False
    return verified

def verify_session_id_by_user_email(cursor, session_id, user_email):
    command = '''SELECT session_id FROM sessions
                  WHERE session_id = ?
                  AND user_id IN
                  (
                      SELECT user_id FROM users
                      WHERE email_address = ?)'''
  
    data = cursor.execute(command, [session_id, user_email])
    data = [d for d, *_ in data]
    verified = data and data[0] == session_id
    if not verified:
        verified = False
    return verified

def add_user(cursor, user_data):
    command = '''INSERT INTO users
                (first_name, last_name, gender, join_date, dob, email_address, pw_salt, pw_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    #hash password
    *user_data, salt, password = user_data
    hashed_password = crypto.hash_string(password, salt)
    user_data = user_data + [salt, hashed_password]

    cursor.execute(command, user_data)

def update_user(cursor, user_data, user_id):
    '''user_data needs to be a full set of user_data, without the user_id, which is passed separately'''
    user_data.append(user_id)
    command = '''UPDATE users
                SET
                    first_name = ?,
                    last_name = ?,
                    gender = ?,
                    join_date = ?,
                    dob = ?,
                    email_address = ?,
                    pw_salt = ?,
                    pw_hash = ?
                WHERE user_id = ?'''
    cursor.execute(command, user_data)

def update_user_by_user_email(cursor, user_data, user_email):
    '''user_data needs to be a full set of user_data, without the user_id, which is passed separately'''
    user_data.append(user_email)
    command = '''UPDATE users
                SET
                    first_name = ?,
                    last_name = ?,
                    gender = ?,
                    join_date = ?,
                    dob = ?,
                    email_address = ?,
                    pw_salt = ?,
                    pw_hash = ?
                WHERE email_address = ?'''
    cursor.execute(command, user_data)

def add_transaction(cursor, transaction_data, chosen_product_ids):
    product_prices = query_product_price_from_product_table(cursor, chosen_product_ids)
    cost = sum(product_prices)
    transaction_data.append(cost)

    command = 'INSERT INTO transactions (user_id, date, cost) VALUES (?, ?, ?)'
    cursor.execute(command, transaction_data)
    
    transaction_id = get_last_added_transaction_id_from_transactions_table(cursor)

    command = 'INSERT INTO detailed_transactions (transaction_id, product_id) VALUES (?, ?)'
    for chosen_product_id in chosen_product_ids:
        cursor.execute(command, [transaction_id, chosen_product_id])
    
def add_session(cursor, session_data):
    command = 'INSERT INTO sessions (session_id, user_id, timestamp) VALUES (?, ?, ?)'
    cursor.execute(command, session_data)

def add_product(cursor, product_data):
    command = 'INSERT INTO products (name, price) VALUES (?, ?)'
    cursor.execute(command, product_data)

def create_user_table(cursor):
    #remove table
    cursor.execute('''DROP TABLE IF EXISTS users''')

    #create table
    cursor.execute('''CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL, 
                     last_name TEXT NOT NULL,
                     gender TEXT,
                     join_date TEXT NOT NULL,
                     dob TEXT CHECK(CAST(strftime('%s', join_date)  AS  integer) > 
                                     CAST(strftime('%s', dob)  AS  integer)),
                     email_address TEXT NOT NULL UNIQUE,
                     pw_salt NOT NULL,
                     pw_hash NOT NULL
                     CHECK (email_address LIKE '%_@_%._%')
                     )''')
 
    #remove index based on user id
    cursor.execute('''DROP INDEX IF EXISTS idx_user_id''')

    #create index based on user_id
    cursor.execute('''CREATE INDEX idx_user_id ON users(user_id)''')


def create_transactions_table(cursor):
    #remove table
    cursor.execute('''DROP TABLE IF EXISTS transactions''')

    #create table
    cursor.execute('''CREATE TABLE transactions (
                    transaction_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    date TEXT,
                    cost REAL NOT NULL,
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                    )''')

    #drop index based on user_id
    cursor.execute('''DROP INDEX IF EXISTS idx_user_id''')

    #create index based on user_id
    cursor.execute('''CREATE INDEX idx_user_id ON transactions(user_id)''')


def create_detailed_transactions_table(cursor):
    #remove table
    cursor.execute('''DROP TABLE IF EXISTS detailed_transactions''')

    #create table
    cursor.execute('''CREATE TABLE detailed_transactions (
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
                    ''')


def create_products_table(cursor):
    #remove table
    cursor.execute('''DROP TABLE IF EXISTS products''')

    #create table
    cursor.execute('''CREATE TABLE products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT,
                    price REAL NOT NULL
                    )''')


def create_sessions_table(cursor):
    #remove table
    cursor.execute('''DROP TABLE IF EXISTS sessions''')

    #create table
    cursor.execute('''CREATE TABLE sessions(
                    session_id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    timestamp TEXT,
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                    )''')
