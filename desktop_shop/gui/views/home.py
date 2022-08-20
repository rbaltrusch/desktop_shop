# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:05:23 2021

@author: richa
"""
import functools

from desktop_shop import gui, server
from desktop_shop.gui import components


class View(components.View):
    """Home view"""

    def init_product_data(self, window: components.Tk, builder: components.Builder):
        """Dynamically generates all contents of the home view"""
        builder.view = self

        with gui.db_conn as cursor:
            product_datas = server.query_product_data_from_product_table(cursor)

        for i, (product_id, name, price) in enumerate(product_datas, 1):
            builder.root = window
            frame = builder.create("menu_frame")
            frame.place(row=i, row_span=1, col=1, col_span=3, sticky="we")
            builder.root = frame.component.tk_component

            # product name label
            label = builder.create("label", width=40, text=f"{name:>30} ${price:<7}")
            label.place(row=i, col=0, sticky="w")

            # add to cart button
            callback = functools.partial(self.add_to_cart, product_id)
            button = builder.create("button", text="Add to cart", command=callback, bd=3)
            button.place(row=i, col=2, sticky="e")

    @staticmethod
    def add_to_cart(product_id):
        """Callback for Add to Cart button. Appends the product id to cart
        and shows checkout button
        """
        gui.app.data["cart"].append(str(product_id))
        if gui.app["main_menu"]["checkout_button"].hidden:
            gui.app["main_menu"].unhide_components("checkout_button")
