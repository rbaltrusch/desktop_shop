# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:31:48 2020

@author: Korean_Crimson
"""

import crypto

def get_user_ids_from_user_table(cursor):
    user_ids = [user_id[0] for user_id in cursor.execute('SELECT user_id FROM users')]
    return user_ids

def verify_session_id(cursor, session_id):
    data = cursor.execute('SELECT session_id FROM sessions WHERE session_id = ?', session_id)
    verified = data and data[0] == session_id
    return verified

def add_user(cursor, user_data):
    command = '''INSERT INTO users
                (first_name, last_name, gender, join_date, dob, email_address, pw_salt, pw)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    #hash password
    *user_data, salt, password = user_data
    hashed_password = crypto.hash_string(password, salt)
    user_data = user_data + [salt, hashed_password]

    cursor.execute(command, user_data)

def update_user(cursor, user_data):
    '''user_data needs to start with user_id and the rest be a full set of user_data'''
    command = '''UPDATE users '''
    cursor.execute(command, user_data)

def add_transaction(cursor, transaction_data):
    command = 'INSERT INTO transactions (user_id, date, cost) VALUES (?, ?, ?)'
    cursor.execute(command, transaction_data)

def add_session(cursor, session_data):
    command = 'INSERT INTO sessions (session_id, user_id, timestamp) VALUES (?, ?, ?)'
    cursor.execute(command, session_data)

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
                     pw NOT NULL
                     CHECK (email_address LIKE '%_@_%._%')
                     )''')
 
    #remove index based on user id
    cursor.execute('''DROP INDEX IF EXISTS idx_user_id''')

    #create index based on user_id
    cursor.execute('''CREATE INDEX idx_user_id ON users(user_id)''')

def create_transaction_table(cursor):
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

def create_products_table(cursor):
    pass

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
                        ON DELETE RESTRICT
                    )''')
