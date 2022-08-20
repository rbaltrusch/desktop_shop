# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 21:48:24 2021

@author: richa
"""

import pytest


@pytest.fixture
def pepper():
    return "secret"
