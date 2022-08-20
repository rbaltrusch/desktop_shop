# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:41 2021

@author: richa
"""
import functools
import tkinter as tk

from desktop_shop import gui, server
from desktop_shop.gui import callbacks, components


# pylint: disable=no-member
class View(components.View):
    """Checkout view"""

    def init_checkout(self):
        """Dynamically generates all contents of the checkout view"""
        chosen_product_ids = gui.app.data["cart"]
        gui.app.builder.view = self

        for frame in self._frame_components.values():
            frame.hide()
        self._frame_components = {}

        with gui.db_conn as cursor:
            args = cursor, chosen_product_ids
            product_datas = server.query_product_data_from_product_table_by_product_ids(*args)

        data_packets = [
            (str(id_), name, price)
            for id_, name, price in product_datas
            if str(id_) in chosen_product_ids
        ]

        i = 0
        for i, (product_id, name, price) in enumerate(data_packets, 1):
            gui.app.builder.root = gui.root
            frame = gui.app.builder.create("frame", name=product_id, relief=tk.RAISED, bd=3)
            frame.place(row=i, row_span=1, col=1, col_span=3, sticky="we")
            gui.app.builder.root = frame.component.tk_component

            # product information label
            full_product_name = f"{name} (#{product_id}):"
            full_text = f"#{i:<3} {full_product_name:<25} ${price:<7}"
            gui.app.builder.create("label", width=42, text=full_text).place(
                row=i, col=0, sticky="w"
            )

            # remove from cart button
            callback = functools.partial(self.remove_from_cart, product_id)
            button = gui.app.builder.create(
                "button", text="Remove from cart", command=callback, bd=3
            )
            button.place(row=i, col=2, sticky="e")

        # confirm transaction button
        gui.app.builder.root = gui.root
        frame = gui.app.builder.create("frame")
        frame.place(row=i + 1, col=3)
        gui.app.builder.root = frame.component.tk_component
        gui.app.builder.create(
            "button2",
            name="checkout",
            text="Confirm transaction",
            command=self.place_order,
            bd=3,
        ).place(sticky="we")

    def remove_from_cart(self, product_id):
        """Callback for dynamically generated remove product from cart button. Gets
        the product to remove directly from the button_name (kind of hacky...),
        removes all dynamically generated widgets on the same row as the button and then
        repacks all other components to fill the resulting gap
        """
        gui.app.data["cart"].remove(product_id)
        frame = self._frame_components.pop(f"{product_id}_frame")
        frame.hide()

        for i, frame in enumerate(self._frame_components.values(), 1):
            frame.row = i
        gui.app["checkout"].repack()

        if not gui.app.data["cart"]:
            gui.app["main_menu"].hide_components("checkout_button")
            callbacks.switch_to_home()

    @staticmethod
    def place_order():
        """Gets all product ids stored in the user cart and sends a transaction request to the
        server. If the server does not answer with a valid session id, the transaction failed
        and an error message is shown, else a confirmation message is shown to the user
        """
        user_email = gui.app.data["user_data"].email
        chosen_product_ids = gui.app.data["cart"]
        if user_email and chosen_product_ids:
            session_id = gui.app.data["session_id"]

            with gui.db_conn as cursor:
                # pylint: disable=redundant-keyword-arg
                # pylint: disable=unexpected-keyword-arg
                # pylint: disable=unpacking-non-sequence
                new_session_id, _ = server.add_transaction(
                    cursor,
                    user_email,
                    chosen_product_ids,
                    user_email=user_email,
                    session_id=session_id,
                )

            gui.app.data["session_id"] = new_session_id
            if new_session_id is not None:
                callbacks.show_message("We have placed your order.")
                gui.app.data["cart"] = []
                gui.app.views_dict["checkout"].clear()
                gui.app["main_menu"].hide_components("checkout_button")
            else:
                callbacks.show_error_message("Your session has expired.")
        else:
            callbacks.show_error_message("We were not able to place your order.")
        callbacks.switch_to_home()
