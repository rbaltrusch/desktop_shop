# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:14:53 2020

@author: Korean_Crimson
"""

import tkinter as tk
from util import DataBaseConnection

class Tk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.col_num = 0
        self.row_num = 0

    def add_row(self, minsize, weight=1):
        self.rowconfigure(self.row_num, minsize=minsize, weight=weight)
        self.row_num += 1

    def add_col(self, minsize, weight=1):
        self.columnconfigure(self.col_num, minsize=minsize, weight=weight)
        self.col_num += 1

class Gui:
    def __init__(self, views_dict, window):
        self.window = window
        self.views_dict = views_dict

    def __enter__(self):
        self.pack_all()
        return self

    def __exit__(self, *_):
        pass

    def mainloop(self):
        self.window.mainloop()

    def pack_all(self):
        for view in self.views_dict.values():
            if view.active:
                view.pack()

class View():
    def __init__(self):
        self.active = False
        self._components = []

    def __iter__(self):
        for component in self._components:
            yield component

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_component(self, component):
        self._components.append(component)

    def get_components(self):
        return self._components

    def pack(self):
        for component in self._components:
            component.gridpack()

class Component():
    def __init__(self, tk_component, row=0, column=0, sticky='n', padx=0, pady=0, column_span=1, row_span=1):
        self.tk_component = tk_component
        self.row = row
        self.column = column
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.column_span = column_span
        self.row_span = row_span

    def gridpack(self):
        self.tk_component.grid(row=self.row, column=self.column, sticky=self.sticky, padx=self.padx, pady=self.padx, rowspan=self.row_span, columnspan=self.column_span)

    def get(self):
        return self.tk_component.get()

def login():
    password = gui.views_dict['login']._components[4].get()
    user_email = gui.views_dict['login']._components[2].get()
    print(user_email, password)

def init_window():
    window = Tk()
    window.title('OfflineShop')
    window.add_row(280)
    window.add_row(20)
    window.add_row(20)
    window.add_row(20)
    window.add_row(20)
    window.add_row(280)
    window.add_col(200)
    window.add_col(100)
    window.add_col(100)
    window.add_col(100)
    window.add_col(200)
    return window

def init_login_view(window):
    login_view = View()

    #login frame
    login_frame = tk.Frame(window, relief=tk.SUNKEN, bd=2)

    #password entry text label
    login_label = tk.Label(login_frame, text="Login", fg="black")
    component = Component(login_label, row=0, column=1)
    login_view.add_component(component, 'login_label')

    #email label
    email_label = tk.Label(login_frame, text='Email address', fg='black')
    component = Component(email_label, row=1, column=0)
    login_view.add_component(component, 'email_label')

    #email entry
    user_email = tk.StringVar()
    user_email_entry = tk.Entry(login_frame, textvariable=user_email)
    component = Component(user_email_entry, row=1, column=1)
    login_view.add_component(component)

    #password label
    password_label = tk.Label(login_frame, text='Password', fg='black')
    component = Component(password_label, row=2, column=0)
    login_view.add_component(component)

    #password entry
    password = tk.StringVar()
    pw_entry = tk.Entry(login_frame, textvariable=password, show="*")
    component = Component(pw_entry, row=2, column=1)
    login_view.add_component(component)

    #login button
    login_button = tk.Button(login_frame, text='Log in', command=login)
    component = Component(login_button, row=3, column=1)
    login_view.add_component(component)

    #add login frame
    component = Component(login_frame, row=1, row_span=4, column=1, column_span=3, sticky='nsew')
    login_view.add_component(component)
    
    return login_view

window = init_window()
login_view = init_login_view(window)
views = {'login': login_view}
login_view.activate()
global cursor

global gui
with Gui(views, tk) as gui, DataBaseConnection('main.db') as cursor:
    gui.mainloop()
