# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:41 2021

@author: richa
"""

import functools
import tkinter as tk

import server
from gui import callbacks, components, app, root, db_conn

class View(components.View):
    @classmethod
    def create(cls, *_):
        '''Initialises an empty checkout view.
    
        Currently, all checkout view contents are dynamically generated in the function
        init_checkout_data_in_checkout_view
        '''
        return cls()

    def init_checkout(self):
        '''Dynamically generates all contents of the checkout view'''
        chosen_product_ids = app.data['cart']
        app.builder.view = self

        for frame in self._frame_components.values():
            frame.hide()
        self._frame_components = {}
    
        with db_conn as cursor:
            product_datas = server.query_product_data_from_product_table_by_product_ids(cursor, chosen_product_ids)

        data_packets = [(str(id_), name, price) for id_, name, price in product_datas if str(id_) in chosen_product_ids]

        for i, (product_id, name, price) in enumerate(data_packets, 1):
            app.builder.root = root
            frame = app.builder.create('frame', name=product_id, relief=tk.RAISED, bd=3)
            frame.place(row=i, row_span=1, col=1, col_span=3, sticky='we')
            app.builder.root = frame.component.tk_component

            #product information label
            full_product_name = f'{name} (#{product_id}):'
            full_text = f'#{i:<3} {full_product_name:<25} ${price:<7}'
            app.builder.create('label', width=42, text=full_text).place(row=i, col=0, sticky='w')

            #remove from cart button
            callback = functools.partial(self.remove_from_cart, product_id)
            button = app.builder.create('button', text='Remove from cart', command=callback, bd=3)
            button.place(row=i, col=2, sticky='e')

        #confirm transaction button
        app.builder.root = root
        frame = app.builder.create('frame')
        frame.place(row=i+1, col=3)
        app.builder.root = frame.component.tk_component
        app.builder.create('button2', name='checkout', text='Confirm transaction',
                           command=self.place_order, bd=3).place(sticky='we')

    def remove_from_cart(self, product_id):
        '''Callback for dynamically generated remove product from cart button. Gets
        the product to remove directly from the button_name (kind of hacky...),
        removes all dynamically generated widgets on the same row as the button and then
        repacks all other components to fill the resulting gap
        '''
        app.data['cart'].remove(product_id)
        frame = self._frame_components.pop(f'{product_id}_frame')
        frame.hide()

        for i, frame in enumerate(self._frame_components.values(), 1):
            frame.row = i
        app['checkout'].repack()

        if not app.data['cart']:
            app['main_menu'].hide_components('checkout_button')
            callbacks.switch_to_home()

    def place_order(self):
        '''Gets all product ids stored in the user cart and sends a transaction request to the
        server. If the server does not answer with a valid session id, the transaction failed
        and an error message is shown, else a confirmation message is shown to the user
        '''
        user_email = app.data['user_data'].email
        chosen_product_ids = app.data['cart']
        if user_email and chosen_product_ids:
            session_id = app.data['session_id']
    
            with db_conn as cursor:
                new_session_id, _ = server.add_transaction(cursor, user_email, chosen_product_ids,
                                                           user_email=user_email,
                                                           session_id=session_id)
    
            app.data['session_id'] = new_session_id
            if new_session_id is not None:
                callbacks.show_message('We have placed your order.')
                app.data['cart'] = []
                app.views_dict['checkout'].clear()
            else:
                callbacks.show_error_message('Your session has expired.')
        else:
            callbacks.show_error_message('We were not able to place your order.')
        callbacks.switch_to_home()
