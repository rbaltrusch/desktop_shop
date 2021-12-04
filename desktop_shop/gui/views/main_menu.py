# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:57:41 2021

@author: richa
"""

import tkinter as tk
from gui import config, callbacks, components
from gui.components import Component

class View(components.View):
    @classmethod
    def create(cls, window):
        '''Initialises main menu view, including all its components'''
        main_menu_view = cls()
    
        #main menu frame
        main_menu_frame = tk.Frame(window, relief=tk.RAISED, bd=3, bg=config.BG2)
        component = Component(main_menu_frame, row=0, column=0, column_span=5, row_span=1, sticky='nsew')
        main_menu_view.add_frame_component(component, 'main_menu_frame')
    
        #home button
        home_button = tk.Button(main_menu_frame, command=callbacks.switch_to_home, text='Home', **config.BUTTON_THEME)
        component = Component(home_button, row=0, column=0)
        main_menu_view.add_component(component, 'home_button')
    
        #login button
        login_button = tk.Button(main_menu_frame, command=callbacks.switch_to_login, text='Login', **config.BUTTON_THEME)
        component = Component(login_button, row=0, column=2, sticky='nsew')
        main_menu_view.add_component(component, 'login_button')
    
        #register button
        register_button = tk.Button(main_menu_frame, command=callbacks.switch_to_register, text='Register', **config.BUTTON_THEME)
        component = Component(register_button, row=0, column=1)
        main_menu_view.add_component(component, 'register_button')
    
        #checkout button
        checkout_button = tk.Button(main_menu_frame, command=callbacks.switch_to_checkout, text='Checkout', **config.BUTTON_THEME)
        component = Component(checkout_button, row=0, column=3)
        main_menu_view.add_component(component, 'checkout_button')
        main_menu_view.hide_component('checkout_button')
    
        #logged in as frame
        logged_in_as_frame = tk.Frame(window, borderwidth=0, highlightthickness=0, bg=config.BG2)
        component = Component(logged_in_as_frame, row=0, column=4, sticky='e')
        main_menu_view.add_frame_component(component, 'logged_in_as_frame')
        main_menu_view.hide_component('logged_in_as_frame')
    
        #options dropdown
        variable = tk.StringVar()
        options = ['Profile', 'Sign out']
        default = 'Logged in as {}'
        variable.set(default)
        variable.trace('w', callbacks.on_dropdown_value_write_event)
        options_dropdown = tk.OptionMenu(logged_in_as_frame, variable, *options)
        options_dropdown['menu'].config(**config.DROPDOWN_THEME)
        component = Component(options_dropdown, row=0, column=7, column_span=2, sticky='nsew', var=variable)
        component.config(**config.DROPDOWN_THEME)
        component.config(highlightthickness=0, bd=3)
        main_menu_view.add_component(component, 'options_dropdown')
    
        #message frame
        message_frame = tk.Frame(window, relief=tk.RIDGE, bd=0, **config.FRAME_THEME)
        component = Component(message_frame, row=0, column=3, column_span=1, sticky='w')
        main_menu_view.add_frame_component(component, 'message_frame')
        main_menu_view.hide_component('message_frame')
    
        #message label
        message = tk.StringVar()
        message_label = tk.Label(message_frame, textvariable=message, **config.LABEL_THEME)
        component = Component(message_label, row=0, column=0, var=message)
        main_menu_view.add_component(component, 'message_label')
    
        #error message label
        error_message = tk.StringVar()
        message_label = tk.Label(message_frame, textvariable=error_message, **config.ERROR_THEME)
        component = Component(message_label, row=0, column=0, var=error_message)
        main_menu_view.add_component(component, 'error_message_label')
        return main_menu_view