# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:31:46 2020

@author: Korean_Crimson
"""

import sqlite3
import time
import datetime

class DataBaseConnection():
    '''Class that wraps the sqlite3 datebase connection, to safely open and close'''
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()

    def __exit__(self, *_):
        self.conn.commit()
        self.conn.close()

    def enter(self):
        '''Calls __enter__ code, use only for cases when contextmanager syntax cannot be used'''
        return self.__enter__()

    def close(self):
        '''Calls __exit__ code, use only for cases when contextmanager syntax cannot be used'''
        self.__exit__()

def timeit(function):
    '''Decorator that prints execution time of a function'''
    def wrapper(*args, **kwargs):
        time0 = time.time()
        result = function(*args, **kwargs)
        print(time.time() - time0)
        return result
    return wrapper

def generate_timestamp():
    '''Generates date+timestamp of current time'''
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def get_current_date():
    '''Returns current date'''
    return datetime.datetime.now().strftime('%Y-%m-%d')

def validate_date_string(date_string):
    '''Checks if passed string can be converted to date'''
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        valid = True
    except ValueError:
        valid = False
    return valid
