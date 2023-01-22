# -*- coding: utf-8 -*-
"""Smoke tests for gui init function"""

# pylint: disable=missing-function-docstring, missing-class-docstring

from collections import namedtuple
import os
import sys

import pytest

from desktop_shop.gui.views import checkout


# pylint: disable=wrong-import-position
from desktop_shop import database, server
from desktop_shop import gui
from desktop_shop.gui import init

Product = namedtuple("Product", ["id", "name", "price"])


def test_gui_init(monkeypatch):
    if sys.platform.startswith("linux") and os.environ.get("DISPLAY") is None:
        pytest.skip()

    def fake_products_query(*_, **__):
        return [
            Product(0, "a", 1000),
            Product(1, "b", 1000),
            Product(2, "c", 1000),
        ]

    monkeypatch.setattr(database, "query_product_data_from_product_table", fake_products_query)
    init.init()
    for view in gui.app.views_dict.values():
        view.pack()


def test_checkout_view():
    if sys.platform.startswith("linux") and os.environ.get("DISPLAY") is None:
        pytest.skip()

    class MonkeyPatch:
        def __enter__(self):
            self.func = server.query_product_data_from_product_table_by_product_ids
            server.query_product_data_from_product_table_by_product_ids = lambda *_, **__: [
                Product(id="0", name="prod", price=3)
            ]

        def __exit__(self, *_):
            server.query_product_data_from_product_table_by_product_ids = self.func

    checkout_view = checkout.View.create(gui.root, init.init_builder())
    with MonkeyPatch():
        gui.app.data["cart"] = ["0"]
        checkout_view.init_checkout()

        # call again to cover code for the case of an already-built checkout View
        checkout_view.init_checkout()
