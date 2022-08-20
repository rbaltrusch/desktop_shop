# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:52:44 2021

@author: Korean_Crimson
"""
import os

from desktop_shop.datagen import generate_data
from desktop_shop.gui import app, db_conn, init

# fast db generation if not present
if not os.path.exists("main.db"):
    generate_data.generate(hash_iterations=1, transactions=100_000, users=10_000, products=20)

try:
    init.init()
    app.views_dict["main_menu"].pack()
    app.views_dict["home"].pack()
    app.mainloop()
finally:
    db_conn.close()
