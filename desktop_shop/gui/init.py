# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:00:48 2021

@author: Korean_Crimson
"""
import tkinter as tk
from typing import Dict

from desktop_shop import gui, user
from desktop_shop.gui import components, config
from desktop_shop.gui.components import Builder, Component, EntryFactory, Factory, Frame
from desktop_shop.gui.views import views


def init_root():
    """Initialises and configures tk root"""
    gui.root.title("OfflineShop")
    gui.root.wm_attributes("-transparentcolor", "purple")
    gui.root.config(bg=config.BG)
    for _ in range(21):
        gui.root.add_row(30)
    for col in [150, 100, 100, 100, 150]:
        gui.root.add_col(col)


def init_builder():
    """Initialises the component builder and registers the widget factories"""
    return Builder(
        frame=Factory(tk.Frame, Frame, kwargs=config.FRAME_THEME),
        menu_frame=Factory(tk.Frame, Component, kwargs=config.MENU_THEME),
        label=EntryFactory(tk.Label, Component, kwargs=config.LABEL_THEME),
        label2=EntryFactory(tk.Label, Component, kwargs=config.ERROR_THEME),
        entry=EntryFactory(tk.Entry, Component, kwargs=config.ENTRY_THEME),
        button=Factory(tk.Button, Component, kwargs=config.BUTTON_THEME),
        button2=Factory(tk.Button, Component, kwargs=config.BUTTON_THEME2),
    )


def init_views(window: components.Tk, builder: components.Builder) -> Dict[str, components.View]:
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
