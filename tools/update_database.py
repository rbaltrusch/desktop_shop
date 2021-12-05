# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:57:30 2020

@author: Korean_Crimson
"""

from util import DataBaseConnection

def update_database():
    with DataBaseConnection('main.db') as cursor:
        command = '''SELECT user_id FROM users
                    WHERE  
                    CAST(strftime('%s', join_date)  AS  integer) <= CAST(strftime('%s', dob)  AS  integer)
                    LIMIT 10;'''
        data = cursor.execute(command)
        for row in data:
            print(row)

if __name__ == '__main__':
    update_database()
