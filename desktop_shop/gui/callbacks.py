# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:53:07 2021

@author: Korean_Crimson
"""
import re

import util
import server
from gui import app, cursor

def login():
    password = app.views_dict['login'].get('pw_entry').get()
    user_email = app.views_dict['login'].get('email_entry').get()
    session_id = server.login(cursor, user_email, password)
    if session_id is not None:
        app.data['session_id'] = session_id
        app.views_dict['login'].hide_component('login_failed_label')
        switch_to_home()
        session_id, user_data = server.query_user_data(cursor, user_email, user_email=user_email, session_id=session_id)
        app.data['session_id'] = session_id
        store_user_data(user_data)
        app.views_dict['main_menu'].unhide_component('logged_in_as_frame')
        app.views_dict['main_menu'].hide_component('message_frame')
        app.views_dict['main_menu'].hide_component('login_button')
        app.views_dict['main_menu'].hide_component('register_button')
        set_logged_in_as_user_text()
        clear_login_data()
    else:
        app.views_dict['login'].unhide_component('login_failed_label')

def sign_out():
    clear_user_data()
    clear_login_data()
    clear_register_data()
    app.views_dict['checkout'].clear()
    app.views_dict['main_menu'].hide_component('logged_in_as_frame')
    app.views_dict['main_menu'].hide_component('message_frame')
    app.views_dict['main_menu'].unhide_component('login_button')
    app.views_dict['main_menu'].unhide_component('register_button')
    app.views_dict['main_menu'].hide_component('checkout_button')
    switch_to_home()

def set_logged_in_as_user_text():
    first_name, last_name = app.data['user_first_name'], app.data['user_last_name']
    full_name = f'{first_name} {last_name}'
    app.views_dict['main_menu'].get('options_dropdown').set_var('Logged in as {}'.format(full_name))

def register():
    register_view = app.views_dict['register']
    email_address = register_view.get('email_entry').get_var()
    first_name = register_view.get('first_name_entry').get_var()
    last_name = register_view.get('last_name_entry').get_var()
    gender = register_view.get('gender_entry').get_var()
    dob = register_view.get('dob_entry').get_var()
    password = register_view.get('pw_entry').get_var()
    confirm_password = register_view.get('confirm_pw_entry').get_var()
    
    join_date = util.get_current_date()
    user_data = [first_name, last_name, gender, join_date, dob, email_address, password]
    valid_data = validate_user_data(user_data)
    valid_password = validate_password(password, confirm_password)
    if valid_data and valid_password:
        session_id = server.add_user(cursor, user_data)
        app.data['session_id'] = session_id
        if session_id is None:
            show_error_message('Failed to register.')
        else:
            #log in
            app.views_dict['login'].get('pw_entry').set_var(password)
            app.views_dict['login'].get('email_entry').set_var(email_address)
            login()
            clear_register_data()

def edit_user_data():
    profile_view = app.views_dict['profile']
    first_name = profile_view.get('first_name_entry').get_var()
    last_name = profile_view.get('last_name_entry').get_var()
    gender = profile_view.get('gender_entry').get_var()
    join_date = profile_view.get('date_joined_data_label').get_var()
    user_email = profile_view.get('email_entry').get_var()
    dob = profile_view.get('dob_entry').get_var()

    user_data = [first_name, last_name, gender, join_date, dob, user_email]
    valid_data = validate_user_data(user_data)
    if valid_data:
        session_id = app.data['session_id']
        user_data = [first_name, last_name, gender, dob, user_email]
        new_session_id, *_ = server.update_user(cursor, user_data, user_email, user_email=user_email, session_id=session_id)
        app.data['session_id'] = new_session_id
        store_user_data([first_name, last_name, gender, join_date, user_email, dob])
        populate_profile_with_user_data()
        if not new_session_id:
            show_error_message('Failed to edit data.')

def edit_user_password():
    profile_view = app.views_dict['profile']
    password = profile_view.get('pw_entry').get_var()
    confirm_password = profile_view.get('confirm_pw_entry').get_var()
    valid_password = validate_password(password, confirm_password)
    if valid_password:
        session_id = app.data['session_id']
        user_email = app.data['user_email']
        new_session_id, *_ = server.update_user_password(cursor, password, user_email, user_email=user_email, session_id=session_id)
        app.data['session_id'] = new_session_id
        if not new_session_id:
            show_error_message('Failed to edit password.')
        else:
            show_message('Set new password successfully.')
            profile_view.get('confirm_pw_entry').set_var('')
            profile_view.get('pw_entry').set_var('')
            profile_view.hide_component('password_change_frame')
            profile_view.unhide_component('password_change_frame_button')

def validate_user_data(user_data):
    first_name, last_name, gender, _, dob, email_address, *_ = user_data

    #validate email
    found_email = re.findall('.+?@.+\..+', email_address)
    if not found_email:
        show_error_message('Email needs to be of the format address@domain.')
        return False

    #validate first_name
    found_first_name = re.findall('\w+?', first_name)
    if not found_first_name:
        show_error_message('First name needs to be alphabetic.')
        return False

    #validate last_name
    found_last_name = re.findall('\w+?', last_name)
    if not found_last_name:
        show_error_message('Last name needs to be alphabetic.')
        return False

    #validate gender
    found_gender = re.findall('[mf]', gender)
    if gender and not found_gender:
        show_error_message('Gender needs to be m or f.')
        return False

    #validate dob
    if dob and not util.validate_date_string(dob):
        show_error_message('Date of birth needs to be in the format YYYY-MM-DD.')
        return False

    return True

def validate_password(password, confirm_password):
    #validate pw
    if len(password) < 8:
        show_error_message('Password needs to be at least 8 characters long.')
        return False
    elif not password == confirm_password:
        show_error_message("Passwords don't match.")
        return False

    return True

def place_order():
    user_email = app.data['user_email']
    chosen_product_ids = app.data['cart']
    if user_email and chosen_product_ids:
        session_id = app.data['session_id']
        new_session_id, _ = server.add_transaction(cursor, user_email, chosen_product_ids, user_email=user_email, session_id=session_id)
        app.data['session_id'] = new_session_id
        if new_session_id is not None:
            show_message('We have placed your order.')
            app.data['cart'] = []
            app.views_dict['checkout'].clear()
        else:
            show_error_message('Your session has expired.')
    else:
        show_error_message('We were not able to place your order.')
    switch_to_home()

def show_message(message):
    main_menu_view = app.views_dict['main_menu']
    main_menu_view.hide_component('error_message_label')
    main_menu_view.get('message_label').set_var(message)
    main_menu_view.unhide_component('message_label')
    main_menu_view.unhide_component('message_frame')

def show_error_message(message):
    main_menu_view = app.views_dict['main_menu']
    main_menu_view.get('error_message_label').set_var(message)
    main_menu_view.hide_component('message_frame')
    main_menu_view.unhide_component('error_message_label')
    main_menu_view.unhide_component('message_frame')

def show_password_change_frame():
    profile_view = app.views_dict['profile']
    profile_view.unhide_component('password_change_frame')
    profile_view.hide_component('password_change_frame_button')

def add_to_cart():
    button_name = app.focused_widget_name
    if button_name is not None:
        *_, product_id = button_name.split('_')
        app.data['cart'].append(product_id)
    if len(app.data['cart']) == 1:
        app.views_dict['main_menu'].unhide_component('checkout_button')

def focus(event):
    app.focused_widget_name = str(event.widget)

def remove_from_cart():
    button_name = app.focused_widget_name
    if button_name is not None:
        *_, row_num, product_id = button_name.split('_')
        app.data['cart'].remove(product_id)
        app.views_dict['checkout'].get(f'product_frame_{row_num}_{product_id}').hide()
        row_counter = 1
        for frame in app.views_dict['checkout'].get_frames():
            if not frame.hidden:
                frame.row = row_counter
                row_counter += 1
        app.views_dict['checkout'].repack()
    if not len(app.data['cart']):
        app.views_dict['main_menu'].hide_component('checkout_button')
        switch_to_home()

def store_user_data(user_data):
    if len(user_data) == 6:
        first_name, last_name, gender, join_date, email_address, dob = user_data
        app.data['user_first_name'] = first_name
        app.data['user_last_name'] = last_name
        app.data['user_gender'] = gender
        app.data['user_join_date'] = join_date
        app.data['user_email'] = email_address
        app.data['user_dob'] = dob

def clear_user_data():
    app.data = init_app_data()

def clear_login_data():
    app.views_dict['login'].get('pw_entry').set_var('')
    app.views_dict['login'].get('email_entry').set_var('')

def clear_register_data():
    register_view = app.views_dict['register']
    register_view.get('email_entry').set_var('')
    register_view.get('first_name_entry').set_var('')
    register_view.get('last_name_entry').set_var('')
    register_view.get('gender_entry').set_var('')
    register_view.get('dob_entry').set_var('')
    register_view.get('pw_entry').set_var('')
    register_view.get('confirm_pw_entry').set_var('')

def switch_to_home():
    app.switch_to('home', 'main_menu')

def switch_to_login():
    app.switch_to('login', 'main_menu')

def switch_to_register():
    app.switch_to('register', 'main_menu')

def switch_to_checkout():
    import init
    init.init_checkout_data_in_checkout_view()
    app.switch_to('checkout', 'main_menu')
    if app.data['session_id'] is None:
        show_error_message('Please login to place your order')

def switch_to_profile():
    populate_profile_with_user_data()
    app.switch_to('profile', 'main_menu')

def activate_profile_entry(entry_name):
    app.views_dict['profile'].get(entry_name).config(state='normal')
    app.views_dict['profile'].get('edit_user_data_button').config(state='normal')
#    app.views_dict['profile'].unhide_component('edit_user_data_button')

def on_dropdown_value_write_event(*args):
    selected_option = app.views_dict['main_menu'].get('options_dropdown').get_var()
    if selected_option == 'Profile':
        switch_to_profile()
        set_logged_in_as_user_text()
    elif selected_option == 'Sign out':
        sign_out()
    app.views_dict['main_menu'].get('options_dropdown').config(state='active')

def populate_profile_with_user_data():
    first_name = app.data['user_first_name']
    last_name = app.data['user_last_name']
    gender = app.data['user_gender']
    join_date = app.data['user_join_date']
    user_email = app.data['user_email']
    dob = app.data['user_dob']

    profile_view = app.views_dict['profile']
    profile_view.get('first_name_entry').set_var(first_name)
    profile_view.get('last_name_entry').set_var(last_name)
    profile_view.get('gender_entry').set_var(gender)
    profile_view.get('date_joined_data_label').set_var(join_date)
    profile_view.get('email_entry').set_var(user_email)
    profile_view.get('dob_entry').set_var(dob)

    profile_view.get('first_name_entry').config(state='disabled')
    profile_view.get('last_name_entry').config(state='disabled')
    profile_view.get('gender_entry').config(state='disabled')
    profile_view.get('date_joined_data_label').config(state='disabled')
    profile_view.get('email_entry').config(state='disabled')
    profile_view.get('dob_entry').config(state='disabled')

#    profile_view.hide_component('edit_user_data_button')
    app.views_dict['profile'].get('edit_user_data_button').config(state='disabled')

def init_gui_data():
    data_dict = {'session_id': None,
                 'user_email': '',
                 'user_first_name': '',
                 'user_last_name': '',
                 'user_dob': '',
                 'user_gender': '',
                 'user_join_date': '',
                 'pw_hash': '',
                 'cart': []}
    return data_dict
