# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:43:01 2021

@author: richa
"""
import tkinter as tk

from desktop_shop import user, util
from desktop_shop.gui import callbacks, components


class View(components.View):
    """Register view"""

    @classmethod
    def create(cls, window: components.Tk, builder: components.Builder):
        """Initialises register view, including all its components"""
        builder.view = cls()
        builder.root = window

        frame = builder.create("frame", name="register", relief=tk.SUNKEN, bd=2)
        frame.place(row=8, row_span=7, col=1, col_span=3, sticky="nsew")
        builder.root = frame.component.tk_component

        builder.create("label", text="Register").place(row=0, col=1)

        # email
        builder.create("label", text="*Email address").place(row=1, col=0)
        entry = builder.create("entry", name="email", textvariable=tk.StringVar())
        entry.place(row=1, col=1, sticky="nsew")

        # first name
        builder.create("label", text="*First name").place(row=2, col=0)
        entry = builder.create("entry", name="first_name", textvariable=tk.StringVar())
        entry.place(row=2, col=1, sticky="nsew")

        # last name
        builder.create("label", text="*Last name").place(row=3, col=0)
        entry = builder.create("entry", name="last_name", textvariable=tk.StringVar())
        entry.place(row=3, col=1, sticky="nsew")

        # gender
        builder.create("label", text="Gender").place(row=4, col=0)
        entry = builder.create("entry", name="gender", textvariable=tk.StringVar())
        entry.place(row=4, col=1, sticky="nsew")

        # date of birth
        builder.create("label", text="Date of Birth").place(row=5, col=0)
        entry = builder.create("entry", name="dob", textvariable=tk.StringVar())
        entry.place(row=5, col=1, sticky="nsew")

        # password
        builder.create("label", text="*Password").place(row=6, col=0)
        entry = builder.create("entry", name="pw", textvariable=tk.StringVar(), show="*")
        entry.place(row=6, col=1, sticky="nsew")

        # confirm pw
        builder.create("label", text="*Confirm Password").place(row=7, col=0)
        entry = builder.create("entry", name="confirm_pw", textvariable=tk.StringVar(), show="*")
        entry.place(row=7, col=1, sticky="nsew")

        builder.create("label", text="*required").place(row=8, col=1)
        builder.create("button2", text="Register", command=callbacks.register).place(row=9, col=1)
        return builder.view

    def clear_entries(self):
        """Clears all entries in the register view"""
        for entry in self.filter("entry"):
            entry.set_var("")

    def get_user_data(self):
        """Returns a UserSignUpData object containing data from register view entries"""
        entry_names = ["first_name", "last_name", "gender", "dob", "email"]
        user_data = user.UserSignUpData(*(self[f"{name}_entry"].get_var() for name in entry_names))
        user_data.join_date = util.get_current_date()
        return user_data
