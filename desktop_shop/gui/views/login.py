# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:04:48 2021

@author: richa
"""
import tkinter as tk

from desktop_shop.gui import callbacks, components


class View(components.View):
    """Login view"""

    @classmethod
    def create(cls, window: components.Tk, builder: components.Builder):
        """Initialises login view, including all its components"""
        builder.view = cls()
        builder.root = window

        # login frame
        frame = builder.create("frame", relief=tk.SUNKEN, bd=2)
        frame.place(row=8, row_span=4, col=1, col_span=3, sticky="nsew")
        builder.root = frame.component.tk_component

        builder.create("label", text="Login").place(row=0, col=1)

        # email
        builder.create("label", text="Email address").place(row=1, col=0)
        edit = builder.create("entry", name="email", textvariable=tk.StringVar())
        edit.place(row=1, col=1, sticky="nsew")

        # password
        builder.create("label", text="Password").place(row=2, col=0)
        edit = builder.create("entry", name="pw", textvariable=tk.StringVar(), show="*")
        edit.place(row=2, col=1, sticky="nsew")

        builder.create("button2", text="Log in", command=callbacks.login).place(row=3, col=1)

        # login unsuccessful
        message = "Logging in has failed. Please check your credentials."
        label = builder.create("label2", name="login_failed", text=message)
        label.place(row=4, col=0, col_span=3)
        builder.view.hide_components("login_failed_label")

        return builder.view

    def clear_entries(self):
        """Clears the password and email entries"""
        for entry in ["pw_entry", "email_entry"]:
            self[entry].set_var("")
