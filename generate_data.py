# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:29:44 2020

@author: Korean_Crimson
"""

import random
import data
import database
import crypto
from util import DataBaseConnection

class UserDataGenerator:
    '''Used to generate data to fill the users table in main.db'''

    def __init__(self):
        self._email_cache = []

    def populate_user_table(self, cursor, number_of_users=10_000):
        '''Populates the user table in main.db (needs to already exist) with the 
        amount of users specified in the input arg. Expects a DataBaseConnection 
        object to be passed in as first arg
        '''
        first_names = data.fetch_first_names()
        last_names = data.fetch_last_names()

        for _ in range(number_of_users):
            user_data = self._generate_random_user_data(first_names, last_names)
            database.add_user(cursor, user_data)

    def _generate_random_user_data(self, first_names, last_names):
        first_name = random.choice(list(first_names.keys()))
        last_name = random.choice(last_names)
        gender = first_names[first_name]
        join_date = data.get_random_date(start=[2014, 6, 1], end=[2020, 11, 1])
        dob = data.get_random_date(start=[1920, 1, 1], end=[2004, 6, 1])
        email_address = self._generate_random_email_address(first_name, last_name, dob)
        salt = crypto.generate_new_salt()
        password = self._generate_new_password()

        user_data = [first_name, last_name, gender, join_date, dob, email_address, salt, password]
        return user_data

    def _generate_random_email_address(self, first_name, last_name, dob):
        '''generates unique email using _email_cache storing all generated emails'''
        email_address = ''
        domains = ['emailook.com', 'oldlurk.com', 'failmailprovider.co.uk', 'beardgamemail.com']
        concatenators = ['-', '_', '.', '', '']
        while not email_address or email_address in self._email_cache:
            domain = random.choice(domains)
            year, *_ = dob.split('-')
            random_string = ''.join([chr(random.randint(65, 90)) for _ in range(random.randint(1, 5))])
            random_num = str(random.randint(0, 999))
            user = random.choices([first_name, last_name, year, random_string, random_num], k=random.randint(2, 4))
            concatenator = random.choice(concatenators)
            email_address = f'{concatenator.join(user)}@{domain}'
        self._email_cache.append(email_address)
        return email_address

    @staticmethod
    def _generate_new_password():
        return 'password'


class TransactionDataGenerator:
    '''Used to generate data to fill the transactions table in main.db'''

    def populate_transactions_table(self, cursor, number_of_transactions=100_000):
        '''Populates the transactions table in main.db (needs to already exist)
        with the amount of transactions specified in the input arg. Expects a
        DataBaseConnection object to be passed in as first arg
        '''
        user_ids = database.get_user_ids_from_user_table(cursor)

        for _ in range(number_of_transactions):
            transaction_data = self._generate_random_transaction_data(user_ids)
            database.add_transaction(cursor, transaction_data)

    @staticmethod
    def _generate_random_transaction_data(user_ids):
        user_id = random.choice(user_ids)
        date = data.get_random_date(start=[2004, 6, 1], end=[2020, 11, 1])
        cost = random.randint(1, 1000*100) / 100 #1 cent resolution

        transaction_data = [user_id, date, cost]
        return transaction_data

def _main():
    #DataBaseConnection automatically saves changes on exit
    with DataBaseConnection('main.db') as cursor:
        #create and populate user table
        database.create_user_table(cursor)
        UserDataGenerator().populate_user_table(cursor)

        #create and populate transactions table
        database.create_transaction_table(cursor)
        TransactionDataGenerator().populate_transactions_table(cursor)

if __name__ == '__main__':
    _main()
