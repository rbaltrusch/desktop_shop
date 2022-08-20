# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:53:07 2021

@author: Korean_Crimson
"""
import re

from desktop_shop import gui, server, user, util

# pylint: disable=E1123,E1124


def login(password=None, email=None):
    """Tries to get a fresh session id from the server by sending password and
    user_email to it. If a new session is granted (password and user_email match),
    gui switches to logged-in home view (login/register button hide, logged-in-as shows)
    """
    password = gui.app["login"]["pw_entry"].get() if password is None else password
    user_email = gui.app["login"]["email_entry"].get() if email is None else email
    with gui.db_conn as cursor:
        session_id = server.login(cursor, user_email, password)

    if session_id is None:
        gui.app.views_dict["login"].unhide_components("login_failed_label")
        return

    gui.app.data["session_id"] = session_id
    gui.app["login"].hide_components("login_failed_label")
    switch_to_home()

    # pylint: disable=unbalanced-tuple-unpacking
    with gui.db_conn as cursor:
        session_id, user_data = server.query_user_data(
            cursor, user_email, user_email=user_email, session_id=session_id
        )

    gui.app.data["session_id"] = session_id
    store_user_data(user_data)
    gui.app["main_menu"].unhide_components("logged_in_as_frame")
    gui.app["main_menu"].hide_components("message_frame", "login_button", "register_button")
    set_logged_in_as_user_text()
    gui.app["login"].clear_entries()


def sign_out():
    """Signs out the currently logged in user. clears the user data, login data,
    register data, checkout basket and returns to not-logged-in home view
    (unhides register/login buttons, hides logged-in-as message)
    """
    gui.app.data = {
        "session_id": None,
        "user_data": user.UserSignUpData(),
        "pw_hash": "",
        "cart": [],
    }
    gui.app["login"].clear_entries()
    gui.app["register"].clear_entries()
    gui.app["checkout"].clear()
    gui.app["main_menu"].hide_components("logged_in_as_frame", "message_frame", "checkout_button")
    gui.app["main_menu"].unhide_components("login_button", "register_button")
    switch_to_home()


def set_logged_in_as_user_text():
    """Sets text of options_dropdown in main menu view to --> Logged in as {full_name}"""
    full_name = gui.app.data["user_data"].full_name
    gui.app["main_menu"]["options_dropdown"].set_var(f"Logged in as {full_name}")


def register():
    """Gets all data entered in the register view and validates it. If valid,
    send the data and the current date to the server and add it to a new user
    in the database, else show an error message
    """
    user_data = gui.app["register"].get_user_data()
    valid_data = validate_user_data(user_data)

    password = gui.app["register"]["pw_entry"].get_var()
    confirm_password = gui.app["register"]["confirm_pw_entry"].get_var()
    valid_password = validate_password(password, confirm_password)

    if not valid_data or not valid_password:
        return

    with gui.db_conn as cursor:
        session_id = server.add_user(cursor, user_data, password)

    gui.app.data["session_id"] = session_id
    if session_id is not None:
        login(password, user_data.email)
        gui.app["register"].clear_entries()
    else:
        show_error_message("Failed to register.")


def edit_user_data():
    """Edits the user data (callback for edit in profile view). Gets all user
    data from the text entries and validates it using validate_user_data. If
    valid, the data is sent to the server. If the server does not respond with
    a valid new session id, the changes failed and a corresponding error message
    is shown.
    """
    user_data = gui.app["profile"].get_user_data()
    valid_data = validate_user_data(user_data)
    if not valid_data:
        return

    session_id = gui.app.data["session_id"]

    with gui.db_conn as cursor:
        user_data_ = user_data[:-1]  # ignore join date
        # pylint: disable=unpacking-non-sequence
        new_session_id, *_ = server.update_user(
            cursor,
            user_data_,
            user_data.email,
            user_email=user_data.email,
            session_id=session_id,
        )

    gui.app.data["session_id"] = new_session_id
    gui.app.data["user_data"] = user_data
    populate_profile_with_user_data()
    if not new_session_id:
        show_error_message("Failed to edit data.")


def edit_user_password():
    """Edits the user password (callback for edit in profile view). Gets the
    password and confirm passwords and validates them. If they are valid, the
    new data is sent to the serer. If the server does not respond with a new
    valid session id, the password change failed and the user is shown an error
    message, else a confirmation message is shown.
    """
    password = gui.app["profile"]["pw_entry"].get_var()
    confirm_password = gui.app["profile"]["confirm_pw_entry"].get_var()
    valid_password = validate_password(password, confirm_password)
    if not valid_password:
        return

    session_id = gui.app.data["session_id"]
    user_email = gui.app.data["user_data"].email

    with gui.db_conn as cursor:
        # pylint: disable=unpacking-non-sequence
        new_session_id, *_ = server.update_user_password(
            cursor, password, user_email, user_email=user_email, session_id=session_id
        )

    gui.app.data["session_id"] = new_session_id
    if not new_session_id:
        show_error_message("Failed to edit password.")
        return

    show_message("Set new password successfully.")
    gui.app["profile"]["confirm_pw_entry"].set_var("")
    gui.app["profile"]["pw_entry"].set_var("")
    gui.app["profile"].hide_components("password_change_frame")
    gui.app["profile"].unhide_components("password_change_frame_button")


def validate_user_data(user_data):
    """Validates all the data entered in the register view. Validates that the
    email is in the correct format, validates that the first and last name are
    alphabetic and not empty, validates that the gender is either m or f and
    validates that the date of birth is a valid date and is not empty
    """
    # validate email
    found_email = re.findall(".+?@.+\\..+", user_data.email)
    if not found_email:
        show_error_message("Email needs to be of the format address@domain.")
        return False

    # validate first_name
    found_first_name = re.findall("\\w+?", user_data.first_name)
    if not found_first_name:
        show_error_message("First name needs to be alphabetic.")
        return False

    # validate last_name
    found_last_name = re.findall("\\w+?", user_data.last_name)
    if not found_last_name:
        show_error_message("Last name needs to be alphabetic.")
        return False

    # validate gender
    found_gender = re.findall("[mf]", user_data.gender)
    if user_data.gender and not found_gender:
        show_error_message("Gender needs to be m or f.")
        return False

    # validate dob
    if user_data.dob and not util.validate_date_string(user_data.dob):
        show_error_message("Date of birth needs to be in the format YYYY-MM-DD.")
        return False

    return True


def validate_password(password, confirm_password):
    """Validates that the passwords match and are longer than 8 characters (returns bool)"""
    if len(password) < 8:
        show_error_message("Password needs to be at least 8 characters long.")
        return False

    if not password == confirm_password:
        show_error_message("Passwords don't match.")
        return False

    return True


def show_message(message):
    """Shows the specified message in the main menu view"""
    gui.app["main_menu"]["message_label"].set_var(message)
    gui.app["main_menu"].hide_components("error_message_label")
    gui.app["main_menu"].unhide_components("message_label", "message_frame")


def show_error_message(message):
    """Shows the specified error message in the main menu view"""
    gui.app["main_menu"]["error_message_label"].set_var(message)
    gui.app["main_menu"].hide_components("message_frame")
    gui.app["main_menu"].unhide_components("error_message_label", "message_frame")


def show_password_change_frame():
    """Callback for change password button in profile view, unhides the password change frame"""
    gui.app["profile"].unhide_components("password_change_frame")
    gui.app["profile"].hide_components("password_change_frame_button")


def store_user_data(user_data):
    """Stores the passed user data in the appropriate gui data fields"""
    if len(user_data) == 6:
        gui.app.data["user_data"] = user.UserSignUpData(*user_data)
    else:
        sign_out()
        show_error_message("Something went wrong while logging in. 2")


def switch_to_home():
    """Switches to home view"""
    gui.app.switch_to("home", "main_menu")


def switch_to_login():
    """Switches to login view"""
    gui.app.switch_to("login", "main_menu")


def switch_to_register():
    """Switches to register view"""
    gui.app.switch_to("register", "main_menu")


def switch_to_checkout():
    """Switches to checkout view. If no valid session id is stored, a warning is given to user"""
    gui.app["checkout"].init_checkout()
    gui.app.switch_to("checkout", "main_menu")
    if gui.app.data["session_id"] is None:
        show_error_message("Please login to place your order")


def switch_to_profile():
    """Switches to the profile view after populating it with the currently logged in user data"""
    populate_profile_with_user_data()
    gui.app.switch_to("profile", "main_menu")


def activate_profile_entry(entry_name):
    """Callback for edit button for the respective field in the user data profile view"""
    gui.app["profile"][entry_name].config(state="normal")
    gui.app["profile"]["edit_user_data_button"].config(state="normal")


def on_dropdown_value_write_event(*_):
    """Callback for options dropdown selection, either switches to profile view or signs out"""
    selected_option = gui.app["main_menu"]["options_dropdown"].get_var()
    if selected_option == "Profile":
        switch_to_profile()
        set_logged_in_as_user_text()
    elif selected_option == "Sign out":
        sign_out()
    gui.app["main_menu"]["options_dropdown"].config(state="active")


def populate_profile_with_user_data():
    """Stores all user data of the currently logged in user in the profile view"""
    gui.app["profile"].store_user_data(gui.app.data["user_data"])
    widget_names = [
        "first_name_entry",
        "last_name_entry",
        "gender_entry",
        "date_joined_data_label",
        "email_entry",
        "dob_entry",
        "edit_user_data_button",
    ]
    for widget_name in widget_names:
        gui.app["profile"][widget_name].config(state="disabled")
