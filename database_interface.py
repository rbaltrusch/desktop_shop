# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:07:42 2020

@author: Korean_Crimson
"""

import database

def edit_user_data(cursor, session_id, user_data):
    verified = database.verify_session_id(cursor, session_id)
    if verified:
        database.