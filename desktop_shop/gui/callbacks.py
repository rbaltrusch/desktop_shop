# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:53:07 2021

@author: Korean_Crimson
"""
import re

import util
import server
from gui import app, db_conn

#pylint: disable=E1123,E1124

def login():
    '''Tries to get a fresh session id from the server by sending password and
    user_email to it. If a new session is granted (password and user_email match),
    gui switches to logged-in home view (login/register button hide, logged-in-as shows)
    '''
    password = app['login']['pw_entry'].get()
    user_email = app['login']['email_entry'].get()
    with db_conn as cursor:
        session_id = server.login(cursor, user_email, password)

    if session_id is not None:
        app.data['session_id'] = session_id
        app['login'].hide_components('login_failed_label')
        switch_to_home()

        #pylint: disable=unbalanced-tuple-unpacking
        with db_conn as cursor:
            session_id, user_data = server.query_user_data(cursor, user_email,
                                                           user_email=user_email,
                                                           session_id=session_id)

        app.data['session_id'] = session_id
        store_user_data(user_data)
        app['main_menu'].unhide_components('logged_in_as_frame')
        app['main_menu'].hide_components('message_frame', 'login_button', 'register_button')
        set_logged_in_as_user_text()
        clear_login_data()
    else:
        app.views_dict['login'].unhide_component('login_failed_label')

def sign_out():
    '''Signs out the currently logged in user. clears the user data, login data,
    register data, checkout basket and returns to not-logged-in home view
    (unhides register/login buttons, hides logged-in-as message)
    '''
    clear_user_data()
    clear_login_data()
    clear_register_data()
    app['checkout'].clear()
    app['main_menu'].hide_components('logged_in_as_frame', 'message_frame', 'checkout_button')
    app['main_menu'].unhide_components('login_button', 'register_button')
    switch_to_home()

def set_logged_in_as_user_text():
    '''Sets text of options_dropdown in main menu view to --> Logged in as {full_name}'''
    first_name, last_name = app.data['user_first_name'], app.data['user_last_name']
    full_name = f'{first_name} {last_name}'
    app['main_menu']['options_dropdown'].set_var(f'Logged in as {full_name}')

def register():
    '''Gets all data entered in the register view and validates it. If valid,
    send the data and the current date to the server and add it to a new user
    in the database, else show an error message
    '''
    email_address = app['register']['email_entry'].get_var()
    first_name = app['register']['first_name_entry'].get_var()
    last_name = app['register']['last_name_entry'].get_var()
    gender = app['register']['gender_entry'].get_var()
    dob = app['register']['dob_entry'].get_var()
    password = app['register']['pw_entry'].get_var()
    confirm_password = app['register']['confirm_pw_entry'].get_var()

    join_date = util.get_current_date()
    user_data = [first_name, last_name, gender, join_date, dob, email_address, password]
    valid_data = validate_user_data(user_data)
    valid_password = validate_password(password, confirm_password)
    if valid_data and valid_password:

        with db_conn as cursor:
            session_id = server.add_user(cursor, user_data)

        app.data['session_id'] = session_id
        if session_id is None:
            show_error_message('Failed to register.')
        else:
            #log in
            app['login']['pw_entry'].set_var(password)
            app['login']['email_entry'].set_var(email_address)
            login()
            clear_register_data()

def edit_user_data():
    '''Edits the user data (callback for edit in profile view). Gets all user
    data from the text entries and validates it using validate_user_data. If
    valid, the data is sent to the server. If the server does not respond with
    a valid new session id, the changes failed and a corresponding error message
    is shown.
    '''
    first_name = app['profile']['first_name_entry'].get_var()
    last_name = app['profile']['last_name_entry'].get_var()
    gender = app['profile']['gender_entry'].get_var()
    join_date = app['profile']['date_joined_data_label'].get_var()
    user_email = app['profile']['email_entry'].get_var()
    dob = app['profile']['dob_entry'].get_var()

    user_data = [first_name, last_name, gender, join_date, dob, user_email]
    valid_data = validate_user_data(user_data)
    if valid_data:
        session_id = app.data['session_id']
        user_data = [first_name, last_name, gender, dob, user_email]

        with db_conn as cursor:
            new_session_id, *_ = server.update_user(cursor, user_data, user_email,
                                                    user_email=user_email, session_id=session_id)

        app.data['session_id'] = new_session_id
        store_user_data([first_name, last_name, gender, join_date, user_email, dob])
        populate_profile_with_user_data()
        if not new_session_id:
            show_error_message('Failed to edit data.')

def edit_user_password():
    '''Edits the user password (callback for edit in profile view). Gets the
    password and confirm passwords and validates them. If they are valid, the
    new data is sent to the serer. If the server does not respond with a new
    valid session id, the password change failed and the user is shown an error
    message, else a confirmation message is shown.
    '''
    password = app['profile']['pw_entry'].get_var()
    confirm_password = app['profile']['confirm_pw_entry'].get_var()
    valid_password = validate_password(password, confirm_password)
    if valid_password:
        session_id = app.data['session_id']
        user_email = app.data['user_email']

        with db_conn as cursor:
            new_session_id, *_ = server.update_user_password(cursor, password, user_email,
                                                             user_email=user_email,
                                                             session_id=session_id)

        app.data['session_id'] = new_session_id
        if not new_session_id:
            show_error_message('Failed to edit password.')
        else:
            show_message('Set new password successfully.')
            app['profile']['confirm_pw_entry'].set_var('')
            app['profile']['pw_entry'].set_var('')
            app['profile'].hide_components('password_change_frame')
            app['profile'].unhide_components('password_change_frame_button')

def validate_user_data(user_data):
    '''Validates all the data entered in the register view. Validates that the
    email is in the correct format, validates that the first and last name are
    alphabetic and not empty, validates that the gender is either m or f and
    validates that the date of birth is a valid date and is not empty
    '''
    first_name, last_name, gender, _, dob, email_address, *_ = user_data

    #validate email
    found_email = re.findall('.+?@.+\\..+', email_address)
    if not found_email:
        show_error_message('Email needs to be of the format address@domain.')
        return False

    #validate first_name
    found_first_name = re.findall('\\w+?', first_name)
    if not found_first_name:
        show_error_message('First name needs to be alphabetic.')
        return False

    #validate last_name
    found_last_name = re.findall('\\w+?', last_name)
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
    '''Validates that the passwords match and are longer than 8 characters (returns bool)'''
    if len(password) < 8:
        show_error_message('Password needs to be at least 8 characters long.')
        return False

    if not password == confirm_password:
        show_error_message("Passwords don't match.")
        return False

    return True

def place_order():
    '''Gets all product ids stored in the user cart and sends a transaction request to the
    server. If the server does not answer with a valid session id, the transaction failed
    and an error message is shown, else a confirmation message is shown to the user
    '''
    user_email = app.data['user_email']
    chosen_product_ids = app.data['cart']
    if user_email and chosen_product_ids:
        session_id = app.data['session_id']

        with db_conn as cursor:
            new_session_id, _ = server.add_transaction(cursor, user_email, chosen_product_ids,
                                                       user_email=user_email,
                                                       session_id=session_id)

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
    '''Shows the specified message in the main menu view'''
    app['main_menu'].hide_component('error_message_label')
    app['main_menu']['message_label'].set_var(message)
    app['main_menu'].unhide_components('message_label', 'message_frame')

def show_error_message(message):
    '''Shows the specified error message in the main menu view'''
    app['main_menu'].get('error_message_label').set_var(message)
    app['main_menu'].hide_components('message_frame')
    app['main_menu'].unhide_components('error_message_label', 'message_frame')

def show_password_change_frame():
    '''Callback for change password button in profile view, unhides the password change frame'''
    app['profile'].unhide_components('password_change_frame')
    app['profile'].hide_components('password_change_frame_button')

def add_to_cart():
    '''Callback for dynamically generated add to cart button in home view. Gets the
    product id directly from the button name (kind of hacky...) and appends the id
    to the cart.
    '''
    button_name = app.focused_widget_name
    if button_name is not None:
        *_, product_id = button_name.split('_')
        app.data['cart'].append(product_id)
    if len(app.data['cart']) == 1:
        app['main_menu'].unhide_components('checkout_button')

def focus(event):
    '''Callback for left-click: stores the currently clicked widget in the app'''
    app.focused_widget_name = str(event.widget)

def remove_from_cart():
    '''Callback for dynamically generated remove product from cart button. Gets
    the product to remove directly from the button_name (kind of hacky...),
    removes all dynamically generated widgets on the same row as the button and then
    repacks all other components to fill the resulting gap
    '''
    button_name = app.focused_widget_name
    if button_name is not None:
        *_, row_num, product_id = button_name.split('_')
        app.data['cart'].remove(product_id)
        app['checkout'][f'product_frame_{row_num}_{product_id}'].hide()
        row_counter = 1
        for frame in app['checkout'].get_frames():
            if not frame.hidden:
                frame.row = row_counter
                row_counter += 1
        app['checkout'].repack()
    if not app.data['cart']:
        app['main_menu'].hide_components('checkout_button')
        switch_to_home()

def store_user_data(user_data):
    '''Stores the passed user data in the appropriate gui data fields'''
    if len(user_data) == 6:
        first_name, last_name, gender, join_date, email_address, dob = user_data
        app.data['user_first_name'] = first_name
        app.data['user_last_name'] = last_name
        app.data['user_gender'] = gender
        app.data['user_join_date'] = join_date
        app.data['user_email'] = email_address
        app.data['user_dob'] = dob
    else:
        sign_out()
        show_error_message('Something went wrong while logging in. 2')

def clear_user_data():
    '''Resets user data stored in gui to default values'''
    app.data = {'session_id': None,
                'user_email': '',
                'user_first_name': '',
                'user_last_name': '',
                'user_dob': '',
                'user_gender': '',
                'user_join_date': '',
                'pw_hash': '',
                'cart': []
                }

def clear_login_data():
    '''Clears all data from the text entries in the login view'''
    app['login']['pw_entry'].set_var('')
    app['login']['email_entry'].set_var('')

def clear_register_data():
    '''Clears all data from the text entries in the register view'''
    app['register']['email_entry'].set_var('')
    app['register']['first_name_entry'].set_var('')
    app['register']['last_name_entry'].set_var('')
    app['register']['gender_entry'].set_var('')
    app['register']['dob_entry'].set_var('')
    app['register']['pw_entry'].set_var('')
    app['register']['confirm_pw_entry'].set_var('')

def switch_to_home():
    '''Switches to home view'''
    app.switch_to('home', 'main_menu')

def switch_to_login():
    '''Switches to login view'''
    app.switch_to('login', 'main_menu')

def switch_to_register():
    '''Switches to register view'''
    app.switch_to('register', 'main_menu')

def switch_to_checkout():
    '''Switches to checkout view. If no valid session id is stored, a warning is given to user'''
    #circular dependency between init and callbacks
    #pylint: disable=import-outside-toplevel
    import gui.init
    gui.init.init_checkout_data_in_checkout_view()
    app.switch_to('checkout', 'main_menu')
    if app.data['session_id'] is None:
        show_error_message('Please login to place your order')

def switch_to_profile():
    '''Switches to the profile view after populating it with the currently logged in user data'''
    populate_profile_with_user_data()
    app.switch_to('profile', 'main_menu')

def activate_profile_entry(entry_name):
    '''Callback for edit button for the respective field in the user data profile view'''
    app['profile'][entry_name].config(state='normal')
    app['profile']['edit_user_data_button'].config(state='normal')

def on_dropdown_value_write_event(*_):
    '''Callback for options dropdown selection, either switches to profile view or signs out'''
    selected_option = app['main_menu']['options_dropdown'].get_var()
    if selected_option == 'Profile':
        switch_to_profile()
        set_logged_in_as_user_text()
    elif selected_option == 'Sign out':
        sign_out()
    app['main_menu']['options_dropdown'].config(state='active')

def populate_profile_with_user_data():
    '''Stores all user data of the currently logged in user in the profile view'''
    first_name = app.data['user_first_name']
    last_name = app.data['user_last_name']
    gender = app.data['user_gender']
    join_date = app.data['user_join_date']
    user_email = app.data['user_email']
    dob = app.data['user_dob']

    app['profile']['first_name_entry'].set_var(first_name)
    app['profile']['last_name_entry'].set_var(last_name)
    app['profile']['gender_entry'].set_var(gender)
    app['profile']['date_joined_data_label'].set_var(join_date)
    app['profile']['email_entry'].set_var(user_email)
    app['profile']['dob_entry'].set_var(dob)

    app['profile']['first_name_entry'].config(state='disabled')
    app['profile']['last_name_entry'].config(state='disabled')
    app['profile']['gender_entry'].config(state='disabled')
    app['profile']['date_joined_data_label'].config(state='disabled')
    app['profile']['email_entry'].config(state='disabled')
    app['profile']['dob_entry'].config(state='disabled')

    app['profile']['edit_user_data_button'].config(state='disabled')
