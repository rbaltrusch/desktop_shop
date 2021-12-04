# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:00:48 2021

@author: Korean_Crimson
"""

import tkinter as tk
import server
from gui.components import Component, View
from gui import app, root, db_conn, callbacks, config

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements
#pylint: disable=line-too-long

def init_main_menu_view(window):
    '''Initialises main menu view, including all its components'''
    main_menu_view = View()

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

def init_login_view(window):
    '''Initialises login view, including all its components'''
    login_view = View()

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

def init_register_view(window):
    '''Initialises register view, including all its components'''
    register_view = View()

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

def init_home_view(_):
    '''Initialises an empty home view.

    Currently, all home view contents are dynamically generated in the function
    init_product_data_in_home_view
    '''
    home_view = View()
    return home_view

def init_product_data_in_home_view():
    '''Dynamically generates all contents of the home view'''
    with db_conn as cursor:
        product_datas = server.query_product_data_from_product_table(cursor)

    home_view = app.views_dict['home']
    for i, (product_id, name, price) in enumerate(product_datas):
        row_num = i + 1

        product_frame = tk.Frame(root, relief=tk.RAISED, bd=3, bg=config.BG2)
        component = Component(product_frame, row=row_num, row_span=1, column=1, column_span=3, sticky='we')
        frame_name = f'product_frame_{product_id}'
        home_view.add_frame_component(component, frame_name)

        #product name label
        product_name_label = tk.Label(product_frame, width=40, text=f'{name:>30} ${price:<7}', **config.LABEL_THEME)
        component = Component(product_name_label, row=row_num, column=0, sticky='w')
        component_name = f'product_name_label_{product_id}'
        home_view.add_component(component, component_name)

        #add to cart button
        component_name = f'add_to_cart_button_{product_id}'
        add_to_cart_button = tk.Button(product_frame, text='Add to cart', command=callbacks.add_to_cart, bd=3, name=component_name, **config.BUTTON_THEME)
        component = Component(add_to_cart_button, row=row_num, column=2, sticky='e')
        home_view.add_component(component, component_name)

def init_checkout_view(_):
    '''Initialises an empty checkout view.

    Currently, all checkout view contents are dynamically generated in the function
    init_checkout_data_in_checkout_view
    '''
    checkout_view = View()
    return checkout_view

def init_checkout_data_in_checkout_view():
    '''Dynamically generates all contents of the checkout view'''
    checkout_view = app.views_dict['checkout']
    chosen_product_ids = app.data['cart']

    with db_conn as cursor:
        product_datas = server.query_product_data_from_product_table_by_product_ids(cursor, chosen_product_ids)

    #adjust for duplicate chosen product ids
    data_packets = []
    for id_ in chosen_product_ids:
        for product_id, name, price in product_datas:
            if str(product_id) == id_:
                data = (product_id, name, price)
                data_packets.append(data)

    row_num = 1
    for i, (product_id, name, price) in enumerate(data_packets, 1):
        row_num = i

        product_frame = tk.Frame(root, relief=tk.RAISED, bd=3, **config.FRAME_THEME)
        component = Component(product_frame, row=row_num, row_span=1, column=1, column_span=3, sticky='we')
        frame_name = f'product_frame_{row_num}_{product_id}'
        checkout_view.add_frame_component(component, frame_name)

        #product information label
        product_id_string = f'(#{product_id})'
        full_product_name = f'{name} {product_id_string}:'
        full_text = f'#{i:<3} {full_product_name:<25} ${price:<7}'
        product_name_label = tk.Label(product_frame, width=42, text=full_text, **config.LABEL_THEME)
        component = Component(product_name_label, row=row_num, column=0, sticky='w')
        component_name = f'product_name_label_{row_num}_{product_id}'
        checkout_view.add_component(component, component_name)

        #add to cart button
        component_name = f'remove_from_cart_button__{row_num}_{product_id}'
        add_to_cart_button = tk.Button(product_frame, text='Remove from cart', command=callbacks.remove_from_cart, bd=3, name=component_name, **config.BUTTON_THEME)
        component = Component(add_to_cart_button, row=row_num, column=2, sticky='e')
        checkout_view.add_component(component, component_name)

    row_num += 1
    #confirm transaction button
    confirm_button = tk.Button(root, text='Confirm transaction', command=callbacks.place_order, bd=3, name=component_name, **config.BUTTON_THEME2)
    component = Component(confirm_button, row=row_num, column=3, sticky='we')
    checkout_view.add_component(component, 'confirm_button')

def init_profile_view(window):
    '''Initialises profile view, including all its components'''
    profile_view = View()

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

def init_root():
    '''Initialises and configures tk root'''
    root.title('OfflineShop')
    root.wm_attributes('-transparentcolor','purple')
    root.bind_all("<Button-1>", callbacks.focus)
    root.config(bg=config.BG)
    for _ in range(21):
        root.add_row(30)
    root.add_col(150)
    root.add_col(100)
    root.add_col(100)
    root.add_col(100)
    root.add_col(150)

def init_views(window):
    '''Initialises all views'''
    views = {'login': init_login_view(window),
             'main_menu': init_main_menu_view(window),
             'home': init_home_view(window),
             'register': init_register_view(window),
             'checkout': init_checkout_view(window),
             'profile': init_profile_view(window)}
    views['home'].activate()
    views['main_menu'].activate()
    return views

def init():
    '''Init function that needs to be called before gui is started'''
    init_root()
    app.views_dict = init_views(root)
    callbacks.clear_user_data()
    init_product_data_in_home_view()
