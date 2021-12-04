# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:02:53 2021

@author: richa
"""
    
import tkinter as tk
from gui import config, callbacks, components
from gui.components import Component

class View(components.View):
    @classmethod
    def create(cls, window):
        '''Initialises profile view, including all its components'''
        profile_view = cls()
    
        date_joined_frame = tk.Frame(window, relief=tk.RAISED, bd=3, **config.FRAME_THEME)
        component = Component(date_joined_frame, row=2, row_span=1, column=1, column_span=3, sticky='nsew')
        profile_view.add_frame_component(component, 'date_joined_frame')
    
        #date joined label
        date_joined_label = tk.Label(date_joined_frame, text="Date joined:", **config.LABEL_THEME)
        component = Component(date_joined_label, row=0, column=0)
        profile_view.add_component(component, 'date_joined_label')
    
        #date joined data label
        date_joined = tk.StringVar()
        date_joined_data_label = tk.Label(date_joined_frame, textvariable=date_joined, **config.LABEL_THEME)
        component = Component(date_joined_data_label, row=0, column=1, var=date_joined, sticky='w')
        profile_view.add_component(component, 'date_joined_data_label')
    
        #profile data frame
        profile_data_frame = tk.Frame(window, relief=tk.RAISED, bd=3, **config.FRAME_THEME)
        component = Component(profile_data_frame, row=3, row_span=6, column=1, column_span=3, sticky='new')
        profile_view.add_frame_component(component, 'profile_data_frame')
    
        #first name label
        first_name_label = tk.Label(profile_data_frame, text="First name:", **config.LABEL_THEME)
        component = Component(first_name_label, row=0, column=0, sticky='w')
        profile_view.add_component(component, 'first_name_label')
    
        #first name data entry
        first_name = tk.StringVar()
        first_name_entry = tk.Entry(profile_data_frame, textvariable=first_name, **config.ENTRY_THEME)
        component = Component(first_name_entry, row=0, column=1, sticky='w', var=first_name)
        component.config(state='disabled')
        profile_view.add_component(component, 'first_name_entry')
    
        #first name edit button
        activate_entry = lambda: callbacks.activate_profile_entry('first_name_entry')
        edit_first_name_button = tk.Button(profile_data_frame, text='Edit', command=activate_entry, bd=3, **config.BUTTON_THEME)
        component = Component(edit_first_name_button, row=0, column=2, sticky='e')
        profile_view.add_component(component, 'first_name_edit_button')
    
    
        #last name label
        last_name_label = tk.Label(profile_data_frame, text="Last name:", **config.LABEL_THEME)
        component = Component(last_name_label, row=1, column=0, sticky='w')
        profile_view.add_component(component, 'last_name_label')
    
        #last name data entry
        last_name = tk.StringVar()
        last_name_entry = tk.Entry(profile_data_frame, textvariable=last_name, **config.ENTRY_THEME)
        component = Component(last_name_entry, row=1, column=1, sticky='w', var=last_name)
        component.config(state='disabled')
        profile_view.add_component(component, 'last_name_entry')
    
        #last name edit button
        activate_entry = lambda: callbacks.activate_profile_entry('last_name_entry')
        edit_last_name_button = tk.Button(profile_data_frame, text='Edit', command=activate_entry, bd=3, **config.BUTTON_THEME)
        component = Component(edit_last_name_button, row=1, column=2, sticky='e')
        profile_view.add_component(component, 'last_name_edit_button')
    
    
        #gender label
        gender_label = tk.Label(profile_data_frame, text="Gender:", **config.LABEL_THEME)
        component = Component(gender_label, row=2, column=0, sticky='w')
        profile_view.add_component(component, 'gender_label')
    
        #gender data entry
        gender = tk.StringVar()
        gender_entry = tk.Entry(profile_data_frame, textvariable=gender, **config.ENTRY_THEME)
        component = Component(gender_entry, row=2, column=1, sticky='w', var=gender)
        component.config(state='disabled')
        profile_view.add_component(component, 'gender_entry')
    
        #gender edit button
        activate_entry = lambda: callbacks.activate_profile_entry('gender_entry')
        edit_gender_button = tk.Button(profile_data_frame, text='Edit', command=activate_entry, bd=3, **config.BUTTON_THEME)
        component = Component(edit_gender_button, row=2, column=2, sticky='e')
        profile_view.add_component(component, 'gender_edit_button')
    
    
        #email label
        email_label = tk.Label(profile_data_frame, text="Email address:", **config.LABEL_THEME)
        component = Component(email_label, row=3, column=0, sticky='w')
        profile_view.add_component(component, 'email_label')
    
        #email data entry
        email = tk.StringVar()
        email_entry = tk.Entry(profile_data_frame, textvariable=email, **config.ENTRY_THEME)
        component = Component(email_entry, row=3, column=1, sticky='w', var=email)
        component.config(state='disabled')
        profile_view.add_component(component, 'email_entry')
    
        #email edit button
        activate_entry = lambda: callbacks.activate_profile_entry('email_entry')
        edit_email_button = tk.Button(profile_data_frame, text='Edit', command=activate_entry, bd=3, **config.BUTTON_THEME)
        component = Component(edit_email_button, row=3, column=2, sticky='e')
        profile_view.add_component(component, 'email_edit_button')
    
    
        #dob label
        dob_label = tk.Label(profile_data_frame, text="Date of Birth:", **config.LABEL_THEME)
        component = Component(dob_label, row=4, column=0, sticky='w')
        profile_view.add_component(component, 'dob_label')
    
        #dob entry
        dob = tk.StringVar()
        dob_entry = tk.Entry(profile_data_frame, textvariable=dob, **config.ENTRY_THEME)
        component = Component(dob_entry, row=4, column=1, sticky='w', var=dob)
        component.config(state='disabled')
        profile_view.add_component(component, 'dob_entry')
    
        #dob edit button
        activate_entry = lambda: callbacks.activate_profile_entry('dob_entry')
        edit_dob_button = tk.Button(profile_data_frame, text='Edit', command=activate_entry, bd=3, **config.BUTTON_THEME)
        component = Component(edit_dob_button, row=4, column=2, sticky='e')
        profile_view.add_component(component, 'dob_edit_button')
    
        #profile data confirm changes button
        edit_user_data_button = tk.Button(profile_data_frame, text='Confirm changes', command=callbacks.edit_user_data, bd=3, **config.BUTTON_THEME2)
        component = Component(edit_user_data_button, row=5, column=1, column_span=2, sticky='nse')
        profile_view.add_component(component, 'edit_user_data_button')
    
    
    
        password_frame = tk.Frame(window, relief=tk.RAISED, bd=3, **config.FRAME_THEME)
        component = Component(password_frame, row=10, row_span=2, column=1, column_span=3, sticky='nsew')
        profile_view.add_frame_component(component, 'password_frame')
    
        password_change_frame_button = tk.Button(password_frame, text='Change password', command=callbacks.show_password_change_frame, bd=3, **config.BUTTON_THEME)
        component = Component(password_change_frame_button, row=4, column=2, sticky='w')
        profile_view.add_component(component, 'password_change_frame_button')
    
    
        password_change_frame = tk.Frame(password_frame, bd=0, **config.FRAME_THEME)
        component = Component(password_change_frame, row=0, row_span=2, column=0, column_span=3)
        profile_view.add_frame_component(component, 'password_change_frame')
        profile_view.hide_component('password_change_frame')
    
        #pw label
        pw_label = tk.Label(password_change_frame, text='*Password', **config.LABEL_THEME)
        component = Component(pw_label, row=0, column=0)
        profile_view.add_component(component, 'pw_label')
    
        #pw entry
        password = tk.StringVar()
        pw_entry = tk.Entry(password_change_frame, textvariable=password, show="*", **config.ENTRY_THEME)
        component = Component(pw_entry, row=0, column=1, sticky='nsew', var=password)
        profile_view.add_component(component, 'pw_entry')
    
        #confirm pw label
        pw_label = tk.Label(password_change_frame, text='*Confirm Password', **config.LABEL_THEME)
        component = Component(pw_label, row=1, column=0)
        profile_view.add_component(component, 'confirm_pw_label')
    
        #confirm pw entry
        confirm_password = tk.StringVar()
        pw_entry = tk.Entry(password_change_frame, textvariable=confirm_password, show="*", **config.ENTRY_THEME)
        component = Component(pw_entry, row=1, column=1, sticky='nsew', var=confirm_password)
        profile_view.add_component(component, 'confirm_pw_entry')
    
        password_change_button = tk.Button(password_change_frame, text='Confirm password change', command=callbacks.edit_user_password, bd=3, **config.BUTTON_THEME2)
        component = Component(password_change_button, row=2, column=1, sticky='e')
        profile_view.add_component(component, 'password_change_button')
        return profile_view