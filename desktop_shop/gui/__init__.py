# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:52:58 2021

@author: Korean_Crimson
"""

import sqlite3
from gui.components import Tk, Gui

root = Tk()
app = Gui(root)
db_conn = sqlite3.connect('main.db')
