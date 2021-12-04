# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:04:48 2021

@author: richa
"""

import tkinter as tk
from gui import config, callbacks, components
from gui.components import Component

class View(components.View):
    @classmethod
    def create(cls, window):
        '''Initialises login view, including all its components'''
        login_view = cls()
    
        #login frame
        login_frame = tk.Frame(window, relief=tk.SUNKEN, bd=2, **config.FRAME_THEME)
        component = Component(login_frame, row=8, row_span=4, column=1, column_span=3, sticky='nsew')
        login_view.add_frame_component(component, 'login_frame')
    
        #password entry text label
        login_label = tk.Label(login_frame, text="Login", **config.LABEL_THEME)
        component = Component(login_label, row=0, column=1)
        login_view.add_component(component, 'login_label')
    
        #email label
        email_label = tk.Label(login_frame, text='Email address', **config.LABEL_THEME)
        component = Component(email_label, row=1, column=0)
        login_view.add_component(component, 'email_label')
    
        #email entry
        user_email = tk.StringVar()
        user_email_entry = tk.Entry(login_frame, textvariable=user_email, **config.ENTRY_THEME)
        component = Component(user_email_entry, row=1, column=1, sticky='nsew', var=user_email)
        login_view.add_component(component, 'email_entry')
    
        #password label
        pw_label = tk.Label(login_frame, text='Password', **config.LABEL_THEME)
        component = Component(pw_label, row=2, column=0)
        login_view.add_component(component, 'pw_label')
    
        #password entry
        password = tk.StringVar()
        pw_entry = tk.Entry(login_frame, textvariable=password, show="*", **config.ENTRY_THEME)
        component = Component(pw_entry, row=2, column=1, sticky='nsew', var=password)
        login_view.add_component(component, 'pw_entry')
    
        #login button
        login_button = tk.Button(login_frame, text='Log in', command=callbacks.login, **config.BUTTON_THEME2)
        component = Component(login_button, row=3, column=1)
        login_view.add_component(component, 'login_button')
    
        #login unsuccessful
        message = 'Logging in has failed. Please check your credentials.'
        login_failed_label = tk.Label(login_frame, text=message, **config.ERROR_THEME)
        component = Component(login_failed_label, row=4, column=0, column_span=3)
        login_view.add_component(component, 'login_failed_label')
        login_view.hide_component('login_failed_label')
        return login_view