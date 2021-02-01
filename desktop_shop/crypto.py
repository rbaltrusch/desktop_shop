# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 20:19:46 2020

@author: Korean_Crimson
"""
import random
import hashlib
import secrets

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def hash_string(password, salt):
    '''Hashes the specified password with the passed salt. Returns hash in hex format (str)'''
    encoded_password = bytes(password, encoding='utf-8')
    encoded_salt = bytes(salt, encoding='utf-8')

    #should be iterations=10000 for security, just changed to 1 for easy database generation
    derived_key = hashlib.pbkdf2_hmac('sha256', encoded_password, encoded_salt, iterations=1)
    return derived_key.hex()

def generate_new_salt():
    '''Generates a new base 62 encoded salt based on a cryptographically
    secure random number, to hash strings.
    '''
    rng = random.SystemRandom()
    random_number = rng.randint(0, 2**64)
    salt = _b62encode(random_number)
    return salt

def _b62encode(num, alphabet=BASE62):
    """Encode a positive number into Base 62 and return the string."""
    char_array = [] if num else [alphabet[0]]
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        char_array.append(alphabet[rem])
    char_array.reverse()
    encoded_string = ''.join(char_array)
    return encoded_string

def generate_new_session_id():
    """Creates a cryptographically-secure, URL-safe string"""
    return secrets.token_urlsafe(16)
