# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 18:57:51 2021

@author: richa
"""

import os
import sys
import runpy
import pytest

@pytest.mark.generate
def test_generate():
    sys.argv.extend(('generate', '--fast', '--minimal'))
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'desktop_shop', 'database.py')
    runpy.run_path(path)

def teardown():
    while len(sys.argv) > 1:
        sys.argv.pop()

    if os.path.isfile('main.db'):
        os.remove('main.db')
