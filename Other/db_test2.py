# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:11:30 2020

@author: Korean_Crimson
"""

import random
import datetime
import sqlite3

first_names = ['Harry', 'John', 'Mary', 'Peter', 'Jane', 'Alice']
last_names = ['Doe', 'Potter', 'Hansel', 'Johnson']

class DB_Connection():
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()
    
    def __exit__(self, *_):
        self.conn.commit()
        self.conn.close()

with DB_Connection('test.db') as cur:
    for data in cur.execute('SELECT * FROM people'):
        print(data)
    
    try:
        cur.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, date TEXT)')
    except Exception:
        pass

    
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    cur.execute('INSERT INTO transactions (first_name, last_name, date) VALUES (?,?,?)', [random.choice(first_names), random.choice(last_names), date])
    
    for data in cur.execute('SELECT * FROM transactions'):
        print(data)

