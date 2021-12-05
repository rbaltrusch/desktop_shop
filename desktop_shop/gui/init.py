# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:00:48 2021

@author: Korean_Crimson
"""

import tkinter as tk
from gui import app, root, callbacks, config, components
from gui.views import login, main_menu, home, register, checkout, profile

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements
#pylint: disable=line-too-long

def init_root():
    '''Initialises and configures tk root'''
    root.title('OfflineShop')
    root.wm_attributes('-transparentcolor','purple')
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

    kwargs = {'relief': tk.RAISED, 'bd': 3, 'bg': config.BG2}
    factory = components.Factory(tk.Frame, components.Component, kwargs=kwargs)
    builder.register('menu_frame', factory)

    factory = components.EntryFactory(tk.Label, components.Component, kwargs=config.LABEL_THEME)
    builder.register('label', factory)

    factory = components.EntryFactory(tk.Label, components.Component, kwargs=config.ERROR_THEME)
    builder.register('label2', factory)

    factory = components.EntryFactory(tk.Entry, components.Component, kwargs=config.ENTRY_THEME)
    builder.register('entry', factory)

    factory = components.Factory(tk.Button, components.Component, kwargs=config.BUTTON_THEME)
    builder.register('button', factory)

    factory = components.Factory(tk.Button, components.Component, kwargs=config.BUTTON_THEME2)
    builder.register('button2', factory)

    return builder

def init_views(window, builder):
    '''Initialises all views'''
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
    app.builder = init_builder()
    app.views_dict = init_views(root, app.builder)
    callbacks.clear_user_data()
    app['home'].init_product_data(root, app.builder)
