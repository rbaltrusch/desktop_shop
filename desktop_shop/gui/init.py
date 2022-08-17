# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:00:48 2021

@author: Korean_Crimson
"""
import tkinter as tk
from typing import Dict

from desktop_shop import gui, user
from desktop_shop.gui import components, config
from desktop_shop.gui.views import views

# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=line-too-long


def init_root():
    """Initialises and configures tk root"""
    gui.root.title("OfflineShop")
    gui.root.wm_attributes("-transparentcolor", "purple")
    gui.root.config(bg=config.BG)
    for _ in range(21):
        gui.root.add_row(30)
    gui.root.add_col(150)
    gui.root.add_col(100)
    gui.root.add_col(100)
    gui.root.add_col(100)
    gui.root.add_col(150)


def init_builder():
    """Initialises the component builder and registers the widget factories"""
    builder = components.Builder()

    factory = components.Factory(tk.Frame, components.Frame, kwargs=config.FRAME_THEME)
    builder.register("frame", factory)

    kwargs = {"relief": tk.RAISED, "bd": 3, "bg": config.BG2}
    factory = components.Factory(tk.Frame, components.Component, kwargs=kwargs)
    builder.register("menu_frame", factory)

    factory = components.EntryFactory(
        tk.Label, components.Component, kwargs=config.LABEL_THEME
    )
    builder.register("label", factory)

    factory = components.EntryFactory(
        tk.Label, components.Component, kwargs=config.ERROR_THEME
    )
    builder.register("label2", factory)

    factory = components.EntryFactory(
        tk.Entry, components.Component, kwargs=config.ENTRY_THEME
    )
    builder.register("entry", factory)

    factory = components.Factory(
        tk.Button, components.Component, kwargs=config.BUTTON_THEME
    )
    builder.register("button", factory)

    factory = components.Factory(
        tk.Button, components.Component, kwargs=config.BUTTON_THEME2
    )
    builder.register("button2", factory)

    return builder


def init_views(
    window: components.Tk, builder: components.Builder
) -> Dict[str, components.View]:
    """Initialises all views"""
    views_: Dict[str, components.View] = {
        name: view.create(window, builder) for name, view in views.items()
    }
    views_["home"].activate()
    views_["main_menu"].activate()
    return views_


def init():
    """Init function that needs to be called before gui is started"""
    init_root()
    gui.app.builder = init_builder()
    gui.app.views_dict = init_views(gui.root, gui.app.builder)
    gui.app.data = {
        "session_id": None,
        "user_data": user.UserSignUpData(),
        "pw_hash": "",
        "cart": [],
    }
    gui.app["home"].init_product_data(gui.root, gui.app.builder)
