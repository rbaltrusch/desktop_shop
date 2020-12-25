# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 14:14:53 2020

@author: Korean_Crimson
"""

import tkinter as tk
import server
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
        self.data = {}
        self.focused_widget_name = None

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
            else:
                view.unpack()

    def deactivate_all(self):
        for view in self.views_dict.values():
            view.deactivate()

    def switch_to(self, *keys):
        self.deactivate_all()
        for key in keys:
            self.views_dict[key].activate()
        self.pack_all()

class View():
    def __init__(self):
        self.active = False
        self._components = {}
        self._frame_components = {}

    def get(self, component_name):
        return self._all_components[component_name]

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_component(self, component, name):
        self._components[name] = component

    def add_frame_component(self, component, name):
        self._frame_components[name] = component

    def pack(self):
#        all_components = {**self._components, **self._frame_components}
        for component in self._all_components.values():
            component.gridpack()

    def unpack(self):
#        all_components = {**self._components, **self._frame_components}
        for component in self._all_components.values():
            component.unpack()

    def hide_component(self, component_name):
        self._all_components[component_name].hide()

    def unhide_component(self, component_name):
        component = self._all_components[component_name]
        component.unhide()
        component.gridpack()

    @property
    def _all_components(self):
        return {**self._components, **self._frame_components}
        

class Component():
    def __init__(self, tk_component, row=0, column=0, sticky='n', padx=0, pady=0, column_span=1, row_span=1, var=None):
        self.tk_component = tk_component
        self.row = row
        self.column = column
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.column_span = column_span
        self.row_span = row_span
        self.hidden = False
        self.var = var
        self.data = None

    def hide(self):
        self.hidden = True
        self.unpack()

    def unhide(self):
        self.hidden = False

    def gridpack(self):
        if not self.hidden:
            self.tk_component.grid(row=self.row, column=self.column, sticky=self.sticky, padx=self.padx, pady=self.padx, rowspan=self.row_span, columnspan=self.column_span)

    def unpack(self):
        self.tk_component.grid_forget()

    def get(self):
        return self.tk_component.get()

    def get_var(self):
        return self.var.get() if self.var else None

    def set_var(self, value):
        if self.var:
            self.var.set(value)

    def config(self, *args, **kwargs):
        self.tk_component.config(*args, **kwargs)


def login():
    password = gui.views_dict['login'].get('pw_entry').get()
    user_email = gui.views_dict['login'].get('email_entry').get()
    session_id = server.login(cursor, user_email, password)
    if session_id is not None:
        gui.data['session_id'] = session_id
        gui.views_dict['login'].hide_component('login_failed_label')
        switch_to_home()
        session_id, user_data = server.query_user_data(cursor, user_email, user_email=user_email, session_id=session_id)
        store_user_data(user_data)
        gui.views_dict['main_menu'].unhide_component('logged_in_as_frame')
        set_logged_in_as_user_text()
    else:
        gui.views_dict['login'].unhide_component('login_failed_label')

def sign_out():
    clear_user_data()
    clear_login_data()
    gui.views_dict['main_menu'].hide_component('logged_in_as_frame')
    switch_to_home()

def set_logged_in_as_user_text():
    first_name, last_name = gui.data['user_first_name'], gui.data['user_last_name']
    full_name = f'{first_name} {last_name}'
    gui.views_dict['main_menu'].get('options_dropdown').set_var('Logged in as {}'.format(full_name))

def register():
    pass

def checkout():
    pass

def add_to_cart():
    button_name = gui.focused_widget_name
    if button_name is not None:
        *_, product_id = button_name.split('_')
        gui.data['cart'].append(product_id)
    if len(gui.data['cart']) == 1:
        gui.views_dict['main_menu'].unhide_component('checkout_button')
    print(gui.data['cart'])

def focus(event):
    gui.focused_widget_name = str(event.widget)

def remove_from_cart():
    pass

def change_user_data():
    pass

def store_user_data(user_data):
    if len(user_data) == 6:
        first_name, last_name, gender, join_date, email_address, dob = user_data
        gui.data['user_first_name'] = first_name
        gui.data['user_last_name'] = last_name
        gui.data['user_gender'] = gender
        gui.data['user_join_date'] = join_date
        gui.data['user_email'] = email_address
        gui.data['user_dob'] = dob

def clear_user_data():
    gui.data = init_gui_data()

def clear_login_data():
    gui.views_dict['login'].get('pw_entry').set_var('')
    gui.views_dict['login'].get('email_entry').set_var('')

def switch_to_home():
    gui.switch_to('home', 'main_menu')

def switch_to_login():
    gui.switch_to('login', 'main_menu')

def switch_to_register():
    gui.switch_to('register', 'main_menu')

def switch_to_checkout():
    if gui.data['session_id'] is not None:
        init_checkout_data_in_checkout_view()
        gui.switch_to('checkout', 'main_menu')
    else:
        print('please log in...')

def switch_to_profile():
    populate_profile_with_user_data()
    gui.switch_to('profile', 'main_menu')

def on_dropdown_value_write_event(*args):
    selected_option = gui.views_dict['main_menu'].get('options_dropdown').get_var()
    if selected_option == 'Profile':
        switch_to_profile()
        set_logged_in_as_user_text()
    elif selected_option == 'Sign out':
        sign_out()
    gui.views_dict['main_menu'].get('options_dropdown').config(state='active')

def populate_profile_with_user_data():
    gui.data['user_first_name']
    gui.data['user_last_name']
    gui.data['user_gender']
    gui.data['user_join_date']
    gui.data['user_email']
    gui.data['user_dob']

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

def init_window():
    window = Tk()
    window.title('OfflineShop')
    window.wm_attributes('-transparentcolor','purple')
    window.bind_all("<Button-1>", focus) 
    window.add_row(30)
    window.add_row(260)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(30)
    window.add_row(130)
    window.add_col(150)
    window.add_col(100)
    window.add_col(100)
    window.add_col(100)
    window.add_col(150)

#    for i in range(10):
#        tk.Frame(window, width=20, height=20, background='#CCCCFF').grid(row=0, column=i)
#
#    for j in range(10):
#        tk.Frame(window, width=20, height=20, background='#CCCCFF').grid(column=0, row=j)
    return window

def init_main_menu_view(window):
    main_menu_view = View()

    #main menu frame
    main_menu_frame = tk.Frame(window, relief=tk.RAISED, bd=3, bg='blue')
    component = Component(main_menu_frame, row=0, column=0, column_span=5, row_span=1, sticky='nsew')
    main_menu_view.add_frame_component(component, 'main_menu_frame')

    #home button
    home_button = tk.Button(main_menu_frame, command=switch_to_home, text='Home', fg='black')
    component = Component(home_button, row=0, column=0)
    main_menu_view.add_component(component, 'home_button')

    #login button
    login_button = tk.Button(main_menu_frame, command=switch_to_login, text='Login', fg='black')
    component = Component(login_button, row=0, column=2, sticky='nsew')
    main_menu_view.add_component(component, 'login_button')

    #register button
    register_button = tk.Button(main_menu_frame, command=switch_to_register, text='Register', fg='black')
    component = Component(register_button, row=0, column=1)
    main_menu_view.add_component(component, 'register_button')

    #checkout button
    checkout_button = tk.Button(main_menu_frame, command=switch_to_checkout, text='Checkout', fg='black')
    component = Component(checkout_button, row=0, column=3)
    main_menu_view.add_component(component, 'checkout_button')
    main_menu_view.hide_component('checkout_button')

    #logged in as frame
    logged_in_as_frame = tk.Frame(window, borderwidth=0, highlightthickness=0, bg='blue')
    component = Component(logged_in_as_frame, row=0, column=4, sticky='e')
    main_menu_view.add_frame_component(component, 'logged_in_as_frame')
    main_menu_view.hide_component('logged_in_as_frame')

    #options dropdown
    variable = tk.StringVar()
    options = ['Profile', 'Sign out']
    default = 'Logged in as {}'
    variable.set(default)
    variable.trace('w', on_dropdown_value_write_event)
    options_dropdown = tk.OptionMenu(logged_in_as_frame, variable, *options)
    component = Component(options_dropdown, row=0, column=7, column_span=2, sticky='nsew', var=variable)
    component.config(bg='blue', fg='white', activebackground='blue', activeforeground='white')
    component.config(highlightthickness=0, bd=3)
    main_menu_view.add_component(component, 'options_dropdown')

    return main_menu_view

def init_login_view(window):
    login_view = View()

    #login frame
    login_frame = tk.Frame(window, relief=tk.SUNKEN, bd=2)
    component = Component(login_frame, row=2, row_span=4, column=1, column_span=3, sticky='nsew')
    login_view.add_frame_component(component, 'login_frame')

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
    component = Component(user_email_entry, row=1, column=1, sticky='nsew', var=user_email)
    login_view.add_component(component, 'email_entry')

    #password label
    pw_label = tk.Label(login_frame, text='Password', fg='black')
    component = Component(pw_label, row=2, column=0)
    login_view.add_component(component, 'pw_label')

    #password entry
    password = tk.StringVar()
    pw_entry = tk.Entry(login_frame, textvariable=password, show="*")
    component = Component(pw_entry, row=2, column=1, sticky='nsew', var=password)
    login_view.add_component(component, 'pw_entry')

    #login button
    login_button = tk.Button(login_frame, text='Log in', command=login)
    component = Component(login_button, row=3, column=1)
    login_view.add_component(component, 'login_button')

    #login unsuccessful
    message = 'Logging in has failed. Please check your credentials.'
    login_failed_label = tk.Label(login_frame, text=message, fg='red')
    component = Component(login_failed_label, row=4, column=0, column_span=3)
    login_view.add_component(component, 'login_failed_label')
    login_view.hide_component('login_failed_label')

    return login_view

def init_register_view(window):
    register_view = View()

    #register frame
    register_frame = tk.Frame(window, relief=tk.SUNKEN, bd=2)
    component = Component(register_frame, row=2, row_span=7, column=1, column_span=3, sticky='nsew')
    register_view.add_frame_component(component, 'register_frame')

    #register label
    register_label = tk.Label(register_frame, text="Register", fg="black")
    component = Component(register_label, row=0, column=1)
    register_view.add_component(component, 'register_label')

    #email label
    email_label = tk.Label(register_frame, text='*Email address', fg='black')
    component = Component(email_label, row=1, column=0)
    register_view.add_component(component, 'email_label')

    #email entry
    user_email = tk.StringVar()
    user_email_entry = tk.Entry(register_frame, textvariable=user_email)
    component = Component(user_email_entry, row=1, column=1, sticky='nsew', var=user_email)
    register_view.add_component(component, 'email_entry')

    #first name label
    first_name_label = tk.Label(register_frame, text='*First name', fg='black')
    component = Component(first_name_label, row=2, column=0)
    register_view.add_component(component, 'first_name_label')

    #first name entry
    first_name = tk.StringVar()
    first_name_entry = tk.Entry(register_frame, textvariable=first_name)
    component = Component(first_name_entry, row=2, column=1, sticky='nsew', var=first_name)
    register_view.add_component(component, 'first_name_entry')

    #last name label
    last_name_label = tk.Label(register_frame, text='*Last name', fg='black')
    component = Component(last_name_label, row=3, column=0)
    register_view.add_component(component, 'last_name_label')

    #last name entry
    last_name = tk.StringVar()
    last_name_entry = tk.Entry(register_frame, textvariable=last_name)
    component = Component(last_name_entry, row=3, column=1, sticky='nsew', var=last_name)
    register_view.add_component(component, 'last_name_entry')

    #gender label
    gender_label = tk.Label(register_frame, text='Gender', fg='black')
    component = Component(gender_label, row=4, column=0)
    register_view.add_component(component, 'gender_label')

    #gender entry
    gender = tk.StringVar()
    gender_entry = tk.Entry(register_frame, textvariable=gender)
    component = Component(gender_entry, row=4, column=1, sticky='nsew', var=gender)
    register_view.add_component(component, 'gender_entry')

    #dob label
    dob_label = tk.Label(register_frame, text='Date of Birth', fg='black')
    component = Component(dob_label, row=5, column=0)
    register_view.add_component(component, 'dob_label')

    #dob entry
    dob = tk.StringVar()
    dob_entry = tk.Entry(register_frame, textvariable=dob)
    component = Component(dob_entry, row=5, column=1, sticky='nsew', var=dob)
    register_view.add_component(component, 'dob_entry')

    #pw label
    pw_label = tk.Label(register_frame, text='*Password', fg='black')
    component = Component(pw_label, row=6, column=0)
    register_view.add_component(component, 'pw_label')

    #pw entry
    password = tk.StringVar()
    pw_entry = tk.Entry(register_frame, textvariable=password, show="*")
    component = Component(pw_entry, row=6, column=1, sticky='nsew', var=password)
    register_view.add_component(component, 'pw_entry')

    #confirm pw label
    pw_label = tk.Label(register_frame, text='*Confirm Password', fg='black')
    component = Component(pw_label, row=7, column=0)
    register_view.add_component(component, 'confirm_pw_label')

    #confirm pw entry
    confirm_password = tk.StringVar()
    pw_entry = tk.Entry(register_frame, textvariable=confirm_password, show="*")
    component = Component(pw_entry, row=7, column=1, sticky='nsew', var=confirm_password)
    register_view.add_component(component, 'confirm_pw_entry')

    #required label
    required_label = tk.Label(register_frame, text="*required", fg="black")
    component = Component(required_label, row=8, column=1)
    register_view.add_component(component, 'required_label')

    #register button
    register_button = tk.Button(register_frame, text='Register', command=register)
    component = Component(register_button, row=9, column=1)
    register_view.add_component(component, 'register_button')

    #login unsuccessful
    message = 'Registering has failed. Please check your credentials.'
    register_failed_label = tk.Label(register_frame, text=message, fg='red')
    component = Component(register_failed_label, row=10, column=0, column_span=3)
    register_view.add_component(component, 'register_failed_label')
    register_view.hide_component('register_failed_label')

    return register_view

def init_home_view(window):
    home_view = View()
    return home_view

def init_product_data_in_home_view():
    product_datas = server.query_product_data_from_product_table(cursor)
    home_view = gui.views_dict['home']
    for i, (product_id, name, price) in enumerate(product_datas):
        row_num = i + 1

        product_frame = tk.Frame(window, relief=tk.RAISED, bd=3)
        component = Component(product_frame, row=row_num, row_span=1, column=1, column_span=3, sticky='nsew')
        frame_name = f'product_frame_{product_id}'
        home_view.add_frame_component(component, frame_name)

        #product name label
        product_name_label = tk.Label(product_frame, text=f'{name:>30}', fg="black")
        component = Component(product_name_label, row=row_num, column=0, sticky='w')
        component_name = f'product_name_label_{product_id}'
        home_view.add_component(component, component_name)

        #product price label
        product_name_label = tk.Label(product_frame, text=f'${price:<50}', fg="black")
        component = Component(product_name_label, row=row_num, column=1, sticky='w')
        component_name = f'product_price_label_{product_id}'
        home_view.add_component(component, component_name)

        #add to cart button
        component_name = f'add_to_cart_button_{product_id}'
        add_to_cart_button = tk.Button(product_frame, text='Add to cart', command=add_to_cart, bg='lightgreen', bd=3, name=component_name)
        component = Component(add_to_cart_button, row=row_num, column=5, sticky='e')
        home_view.add_component(component, component_name)

def init_checkout_view(window):
    checkout_view = View()
    return checkout_view

def init_checkout_data_in_checkout_view():
    checkout_view = gui.views_dict['checkout']
    chosen_product_ids = gui.data['cart']
    product_datas = server.query_product_data_from_product_table_by_product_ids(cursor, chosen_product_ids)
    for i, (product_id, name, price) in enumerate(product_datas, 1):
        row_num = i

        product_frame = tk.Frame(window, relief=tk.RAISED, bd=3)
        component = Component(product_frame, row=row_num, row_span=1, column=1, column_span=3, sticky='nsew')
        frame_name = f'product_frame_{product_id}'
        checkout_view.add_frame_component(component, frame_name)

        #product information label
        product_id_string = f'(#{product_id})'
        full_product_name = f'{name} {product_id_string}:'
#        {name:<15} {product_id_string:>6}:
        full_text = f'#{i:<2} {full_product_name:<20} ${price:<7}'
        product_name_label = tk.Label(product_frame, text=full_text, fg="black")
        component = Component(product_name_label, row=row_num, column=0, sticky='w')
        component_name = f'product_name_label_{product_id}'
        checkout_view.add_component(component, component_name)

        #add to cart button
        component_name = f'remove_from_cart_button_{product_id}'
        add_to_cart_button = tk.Button(product_frame, text='Remove from cart', command=remove_from_cart, bg='orange', bd=3, name=component_name)
        component = Component(add_to_cart_button, row=row_num, column=5, sticky='e')
        checkout_view.add_component(component, component_name)

def init_profile_view(window):
    profile_view = View()

    date_joined_frame = tk.Frame(window, relief=tk.RAISED, bd=3)
    component = Component(date_joined_frame, row=2, row_span=1, column=1, column_span=3, sticky='nsew')
    profile_view.add_frame_component(component, 'date_joined_frame')

    profile_data_frame = tk.Frame(window, relief=tk.RAISED, bd=3)
    component = Component(profile_data_frame, row=3, row_span=7, column=1, column_span=3, sticky='nsew')
    profile_view.add_frame_component(component, 'profile_data_frame')

    password_frame = tk.Frame(window, relief=tk.RAISED, bd=3)
    component = Component(password_frame, row=8, row_span=2, column=1, column_span=3, sticky='nsew')
    profile_view.add_frame_component(component, 'password_frame')

    return profile_view

def init_views(window):
    views = {'login': init_login_view(window),
             'main_menu': init_main_menu_view(window),
             'home': init_home_view(window),
             'register': init_register_view(window),
             'checkout': init_checkout_view(window),
             'profile': init_profile_view(window)}
    views['home'].activate()
    views['main_menu'].activate()
    return views


global cursor
global gui
global window

window = init_window()
views = init_views(window)

with Gui(views, tk) as gui, DataBaseConnection('main.db') as cursor:
    gui.data = init_gui_data()
    init_product_data_in_home_view()
    gui.views_dict['home'].pack()
    gui.mainloop()
