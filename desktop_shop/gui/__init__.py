# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:52:58 2021

@author: Korean_Crimson
"""

from util import DataBaseConnection
from gui.components import Tk, Gui

root = Tk()
app = Gui(root)
db_conn = DataBaseConnection('main.db')
