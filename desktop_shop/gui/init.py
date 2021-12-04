# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:00:48 2021

@author: Korean_Crimson
"""

import tkinter as tk
import server
from gui.components import Component
from gui import app, root, db_conn, callbacks, config, components
from gui.views import login, main_menu, home, register, checkout, profile

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements
#pylint: disable=line-too-long

def init_product_data_in_home_view():
    '''Dynamically generates all contents of the home view'''
    with db_conn as cursor:
        product_datas = server.query_product_data_from_product_table(cursor)

    home_view = app.views_dict['home']
    for i, (product_id, name, price) in enumerate(product_datas):
        row_num = i + 1

        product_frame = tk.Frame(root, relief=tk.RAISED, bd=3, bg=config.BG2)
        component = Component(product_frame, row=row_num, row_span=1, col=1, col_span=3, sticky='we')
        frame_name = f'product_frame_{product_id}'
        home_view.add_frame_component(component, frame_name)

        #product name label
        product_name_label = tk.Label(product_frame, width=40, text=f'{name:>30} ${price:<7}', **config.LABEL_THEME)
        component = Component(product_name_label, row=row_num, col=0, sticky='w')
        component_name = f'product_name_label_{product_id}'
        home_view.add_component(component, component_name)

        #add to cart button
        component_name = f'add_to_cart_button_{product_id}'
        add_to_cart_button = tk.Button(product_frame, text='Add to cart', command=callbacks.add_to_cart, bd=3, name=component_name, **config.BUTTON_THEME)
        component = Component(add_to_cart_button, row=row_num, col=2, sticky='e')
        home_view.add_component(component, component_name)

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
        component = Component(product_frame, row=row_num, row_span=1, col=1, col_span=3, sticky='we')
        frame_name = f'product_frame_{row_num}_{product_id}'
        checkout_view.add_frame_component(component, frame_name)

        #product information label
        product_id_string = f'(#{product_id})'
        full_product_name = f'{name} {product_id_string}:'
        full_text = f'#{i:<3} {full_product_name:<25} ${price:<7}'
        product_name_label = tk.Label(product_frame, width=42, text=full_text, **config.LABEL_THEME)
        component = Component(product_name_label, row=row_num, col=0, sticky='w')
        component_name = f'product_name_label_{row_num}_{product_id}'
        checkout_view.add_component(component, component_name)

        #add to cart button
        component_name = f'remove_from_cart_button__{row_num}_{product_id}'
        add_to_cart_button = tk.Button(product_frame, text='Remove from cart', command=callbacks.remove_from_cart, bd=3, name=component_name, **config.BUTTON_THEME)
        component = Component(add_to_cart_button, row=row_num, col=2, sticky='e')
        checkout_view.add_component(component, component_name)

    row_num += 1
    #confirm transaction button
    confirm_button = tk.Button(root, text='Confirm transaction', command=callbacks.place_order, bd=3, name=component_name, **config.BUTTON_THEME2)
    component = Component(confirm_button, row=row_num, col=3, sticky='we')
    checkout_view.add_component(component, 'confirm_button')

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

def init_builder():
    builder = components.Builder()

    factory = components.Factory(tk.Frame, components.Frame, kwargs=config.FRAME_THEME)
    builder.register('frame', factory)

    factory = components.EntryFactory(tk.Label, components.Component, kwargs=config.LABEL_THEME)
    builder.register('label', factory)

    factory = components.EntryFactory(tk.Entry, components.Component, kwargs=config.ENTRY_THEME)
    builder.register('entry', factory)

    factory = components.EntryFactory(tk.Button, components.Component, kwargs=config.BUTTON_THEME)
    builder.register('button', factory)

    factory = components.EntryFactory(tk.Button, components.Component, kwargs=config.BUTTON_THEME2)
    builder.register('button2', factory)

    return builder

def init_views(window):
    '''Initialises all views'''
    builder = init_builder()
    views = {'login': login.View.create(window, builder),
             'main_menu': main_menu.View.create(window, builder),
             'home': home.View.create(window, builder),
             'register': register.View.create(window, builder),
             'checkout': checkout.View.create(window, builder),
             'profile': profile.View.create(window, builder),
             }
    views['home'].activate()
    views['main_menu'].activate()
    return views

def init():
    '''Init function that needs to be called before gui is started'''
    init_root()
    app.views_dict = init_views(root)
    callbacks.clear_user_data()
    init_product_data_in_home_view()
