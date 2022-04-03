# -*- coding: utf-8 -*-
"""Smoke tests for gui init function"""
import tkinter as tk
from collections import namedtuple

import desktop_shop.gui as gui
import desktop_shop.gui.init as init
import desktop_shop.server as server

Product = namedtuple("Product", ["id", "name", "price"])


def setup():
    class FakeTk:
        pass
    tk.Tk = FakeTk


def test_gui_init():
    init.init()
    for view in gui.app.views_dict.values():
        view.pack()


def test_checkout_view():
    class MonkeyPatch:
        def __enter__(self):
            self.func = server.query_product_data_from_product_table_by_product_ids
            server.query_product_data_from_product_table_by_product_ids = (
                lambda *_, **__: [Product(id="0", name="prod", price=3)]
            )

        def __exit__(self, *_):
            server.query_product_data_from_product_table_by_product_ids = self.func

    with MonkeyPatch():
        gui.app.data["cart"] = ["0"]
        gui.app["checkout"].init_checkout()

        # call again to cover code for the case of an already-built checkout View
        gui.app["checkout"].init_checkout()
