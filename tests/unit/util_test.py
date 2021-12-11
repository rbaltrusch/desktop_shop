# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 17:34:44 2021

@author: richa
"""

import time
import datetime
import pytest

import util

def test_generate_timestamp():
    timestamp = util.generate_timestamp()
    time_ = datetime.datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
    assert time_.timestamp() == pytest.approx(time.time())

def test_get_current_date():
    date = util.get_current_date()
    year, month, day = date.split('-')
    now = datetime.datetime.now()
    assert str(now.year) == year
    assert str(now.month) == month
    assert str(now.day) == day

@pytest.mark.parametrize("string, expected", [("2021-01-01", True),
                                              ("20-01-01", False),
                                              ("01-01-20021", False)])
def test_validate_date_string(string, expected):
    assert util.validate_date_string(string) == expected
