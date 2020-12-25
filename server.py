# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:07:42 2020

@author: Korean_Crimson
"""

import database
import crypto
import util
from util import DataBaseConnection

def verify_database_call(function):
    def wrapper(*args, user_email='', session_id=''):
        cursor, *_ = args
        verified = database.verify_session_id_by_user_email(cursor, session_id, user_email)
        print(session_id, verified)
        if verified:
            results = function(*args)

            #get new session id and add it to database
            new_session_id = _add_new_session(cursor, user_email)
        else:
            new_session_id = None
            results = None
        return new_session_id, results
    return wrapper

@verify_database_call
def query_user_data(cursor, user_email):
    return database.query_user_data_by_user_email(cursor, user_email)

@verify_database_call
def add_user(cursor, user_data):
    return database.add_user(cursor, user_data)

@verify_database_call
def add_transaction(cursor, user_email, chosen_product_ids):
    user_id = database.query_user_id_from_user_email(cursor, user_email)
    date = util.get_current_date()
    transaction_data = [user_id, date]
    return database.add_transaction(cursor, transaction_data, chosen_product_ids)

@verify_database_call
def update_user(cursor, user_data, user_email):
    return database.update_user_by_user_email(cursor, user_data, user_email)

def query_product_data_from_product_table(cursor):
    return database.query_product_data_from_product_table(cursor)

def query_product_data_from_product_table_by_product_ids(cursor, product_ids):
    return database.query_product_data_from_product_table_by_product_ids(cursor, product_ids)

def login(cursor, user_email, password):
    data = database.query_pw_hash_and_salt_by_user_email(cursor, user_email)
    if len(data) == 2:
        pw_salt, pw_hash = data
        verified = crypto.hash_string(password, pw_salt) == pw_hash
        new_session_id = _add_new_session(cursor, user_email) if verified else None
    else:
        new_session_id = None
    return new_session_id

def _add_new_session(cursor, user_email):
    new_session_id = crypto.generate_new_session_id()
    timestamp = util.generate_timestamp()
    user_id = database.query_user_id_from_user_email(cursor, user_email)
    session_data = [new_session_id, user_id, timestamp]
    database.add_session(cursor, session_data)
    return new_session_id

if __name__ == '__main__':
    user_email = 'FLLKX1924796796@emailook.com'
    password = 'password'
    
    with DataBaseConnection('main.db') as cursor:
        #test login
        session_id = login(cursor, user_email, password)

        #test query data
        session_id, user_data = query_user_data(cursor, user_email, user_email=user_email, session_id=session_id)
        for row in user_data:
            print(row)
        
        print()

        #test update data
        first_name, last_name, gender, _, user_email, dob = user_data
        first_name = 'Lemma'
        user_data = [first_name, last_name, gender, dob, user_email]
        session_id, result = update_user(cursor, user_data, user_email, user_email=user_email, session_id=session_id)
        
        session_id, user_data = query_user_data(cursor, user_email, user_email=user_email, session_id=session_id)
        for row in user_data:
            print(row)

        chosen_product_ids = [1, 2, 3]
        session_id, result = add_transaction(cursor, user_email, chosen_product_ids, user_email=user_email, session_id=session_id)
        print(session_id)
