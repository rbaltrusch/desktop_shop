# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:43:01 2021

@author: richa
"""

import tkinter as tk
from gui import config, callbacks, components
from gui.components import Component

class View(components.View):
    @classmethod
    def create(cls, window):
        '''Initialises register view, including all its components'''
        register_view = cls()

        #register frame
        register_frame = tk.Frame(window, relief=tk.SUNKEN, bd=2, **config.FRAME_THEME)
        component = Component(register_frame, row=8, row_span=7, column=1, column_span=3, sticky='nsew')
        register_view.add_frame_component(component, 'register_frame')
    
        #register label
        register_label = tk.Label(register_frame, text="Register", **config.LABEL_THEME)
        component = Component(register_label, row=0, column=1)
        register_view.add_component(component, 'register_label')
    
        #email label
        email_label = tk.Label(register_frame, text='*Email address', **config.LABEL_THEME)
        component = Component(email_label, row=1, column=0)
        register_view.add_component(component, 'email_label')
    
        #email entry
        user_email = tk.StringVar()
        user_email_entry = tk.Entry(register_frame, textvariable=user_email, **config.ENTRY_THEME)
        component = Component(user_email_entry, row=1, column=1, sticky='nsew', var=user_email)
        register_view.add_component(component, 'email_entry')
    
        #first name label
        first_name_label = tk.Label(register_frame, text='*First name', **config.LABEL_THEME)
        component = Component(first_name_label, row=2, column=0)
        register_view.add_component(component, 'first_name_label')
    
        #first name entry
        first_name = tk.StringVar()
        first_name_entry = tk.Entry(register_frame, textvariable=first_name, **config.ENTRY_THEME)
        component = Component(first_name_entry, row=2, column=1, sticky='nsew', var=first_name)
        register_view.add_component(component, 'first_name_entry')
    
        #last name label
        last_name_label = tk.Label(register_frame, text='*Last name', **config.LABEL_THEME)
        component = Component(last_name_label, row=3, column=0)
        register_view.add_component(component, 'last_name_label')
    
        #last name entry
        last_name = tk.StringVar()
        last_name_entry = tk.Entry(register_frame, textvariable=last_name, **config.ENTRY_THEME)
        component = Component(last_name_entry, row=3, column=1, sticky='nsew', var=last_name)
        register_view.add_component(component, 'last_name_entry')
    
        #gender label
        gender_label = tk.Label(register_frame, text='Gender', **config.LABEL_THEME)
        component = Component(gender_label, row=4, column=0)
        register_view.add_component(component, 'gender_label')
    
        #gender entry
        gender = tk.StringVar()
        gender_entry = tk.Entry(register_frame, textvariable=gender, **config.ENTRY_THEME)
        component = Component(gender_entry, row=4, column=1, sticky='nsew', var=gender)
        register_view.add_component(component, 'gender_entry')
    
        #dob label
        dob_label = tk.Label(register_frame, text='Date of Birth', **config.LABEL_THEME)
        component = Component(dob_label, row=5, column=0)
        register_view.add_component(component, 'dob_label')
    
        #dob entry
        dob = tk.StringVar()
        dob_entry = tk.Entry(register_frame, textvariable=dob, **config.ENTRY_THEME)
        component = Component(dob_entry, row=5, column=1, sticky='nsew', var=dob)
        register_view.add_component(component, 'dob_entry')
    
        #pw label
        pw_label = tk.Label(register_frame, text='*Password', **config.LABEL_THEME)
        component = Component(pw_label, row=6, column=0)
        register_view.add_component(component, 'pw_label')
    
        #pw entry
        password = tk.StringVar()
        pw_entry = tk.Entry(register_frame, textvariable=password, show="*", **config.ENTRY_THEME)
        component = Component(pw_entry, row=6, column=1, sticky='nsew', var=password)
        register_view.add_component(component, 'pw_entry')
    
        #confirm pw label
        pw_label = tk.Label(register_frame, text='*Confirm Password', **config.LABEL_THEME)
        component = Component(pw_label, row=7, column=0)
        register_view.add_component(component, 'confirm_pw_label')
    
        #confirm pw entry
        confirm_password = tk.StringVar()
        pw_entry = tk.Entry(register_frame, textvariable=confirm_password, show="*", **config.ENTRY_THEME)
        component = Component(pw_entry, row=7, column=1, sticky='nsew', var=confirm_password)
        register_view.add_component(component, 'confirm_pw_entry')
    
        #required label
        required_label = tk.Label(register_frame, text="*required", **config.LABEL_THEME)
        component = Component(required_label, row=8, column=1)
        register_view.add_component(component, 'required_label')
    
        #register button
        register_button = tk.Button(register_frame, text='Register', command=callbacks.register, **config.BUTTON_THEME2)
        component = Component(register_button, row=9, column=1)
        register_view.add_component(component, 'register_button')
        return register_view
