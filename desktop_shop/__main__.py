# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:52:44 2021

@author: Korean_Crimson
"""
from .gui import app
from .gui import db_conn
from .gui import init

try:
    init.init()
    app.views_dict['main_menu'].pack()
    app.views_dict['home'].pack()
    app.mainloop()
finally:
    db_conn.close()
