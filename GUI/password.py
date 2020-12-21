# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 16:32:36 2020

@author: Korean_Crimson
"""

import tkinter as tk

window = tk.Tk()

password = ''

passwd = tk.Entry(window, textvariable=password, show="*")
passwd.pack()

window.mainloop()