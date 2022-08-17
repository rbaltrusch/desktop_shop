# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:31:46 2020

@author: Korean_Crimson
"""

import datetime


def generate_timestamp() -> str:
    """Generates date+timestamp of current time"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def get_current_date() -> str:
    """Returns current date"""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def validate_date_string(date_string) -> bool:
    """Checks if passed string can be converted to date"""
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        valid = True
    except ValueError:
        valid = False
    return valid
