# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:57:41 2021

@author: richa
"""
import tkinter as tk

from desktop_shop.gui import callbacks, components, config


# pylint: disable=line-too-long
class View(components.View):
    """Main menu view"""

    @classmethod
    def create(cls, window: components.Tk, builder: components.Builder):
        """Initialises main menu view, including all its components"""
        builder.view = cls()
        builder.root = window

        frame = builder.create("menu_frame")
        frame.place(row=0, col=0, col_span=5, row_span=1, sticky="nsew")
        builder.root = frame.component.tk_component

        # buttons
        builder.create("button", name="home", command=callbacks.switch_to_home, text="Home").place(
            row=0, col=0
        )
        builder.create(
            "button",
            name="register",
            command=callbacks.switch_to_register,
            text="Register",
        ).place(row=0, col=1)
        builder.create(
            "button", name="login", command=callbacks.switch_to_login, text="Login"
        ).place(row=0, col=2, sticky="nsew")

        button = builder.create(
            "button",
            name="checkout",
            text="Checkout",
            command=callbacks.switch_to_checkout,
        )
        button.place(row=0, col=3)
        builder.view.hide_components("checkout_button")

        # logged in as frame
        logged_in_as_frame = tk.Frame(window, borderwidth=0, highlightthickness=0, bg=config.BG2)
        component = components.Component(logged_in_as_frame, row=0, col=4, sticky="e")
        builder.view.add_frame_component(component, "logged_in_as_frame")
        builder.view.hide_components("logged_in_as_frame")

        # options dropdown
        variable = tk.StringVar()
        options = ["Profile", "Sign out"]
        variable.set("Logged in as {}")
        variable.trace("w", callbacks.on_dropdown_value_write_event)
        options_dropdown = tk.OptionMenu(logged_in_as_frame, variable, *options)
        options_dropdown["menu"].config(**config.DROPDOWN_THEME)
        component = components.Component(
            options_dropdown, row=0, col=7, col_span=2, sticky="nsew", var=variable
        )
        component.config(**config.DROPDOWN_THEME)
        component.config(highlightthickness=0, bd=3)
        builder.view.add_component(component, "options_dropdown")

        # message frame
        builder.root = window
        frame = builder.create("frame", name="message", relief=tk.RIDGE, bd=0)
        frame.place(row=0, col=3, col_span=1, sticky="w")
        builder.view.hide_components("message_frame")
        builder.root = frame.component.tk_component

        builder.create("label", name="message", textvariable=tk.StringVar()).place(row=0, col=0)
        builder.create("label2", name="error_message", textvariable=tk.StringVar()).place(
            row=0, col=0
        )

        return builder.view
