# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:07:15 2020

@author: Korean_Crimson
"""

import sqlite3
conn = sqlite3.connect('test.db')
cur = conn.cursor()

for data in cur.execute('SELECT * FROM people'):
    print(data)

conn.close()