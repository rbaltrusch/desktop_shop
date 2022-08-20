# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:02:53 2021

@author: richa
"""
import functools
import tkinter as tk
from typing import List

from desktop_shop import user
from desktop_shop.gui import callbacks, components


# pylint: disable=line-too-long
class View(components.View):
    """Profile view"""

    @classmethod
    def create(cls, window: components.Tk, builder: components.Builder):
        """Initialises profile view, including all its components"""
        builder.view = cls()
        builder.root = window

        frame = builder.create("frame", relief=tk.RAISED, bd=3)
        frame.place(row=2, row_span=1, col=1, col_span=3, sticky="nsew")
        builder.root = frame.component.tk_component

        # date joined
        builder.create("label", text="Date joined:").place(row=0, col=0)
        label = builder.create("label", name="date_joined_data", textvariable=tk.StringVar())
        label.place(row=0, col=1, sticky="w")

        # profile data frame
        builder.root = window
        frame = builder.create("frame", relief=tk.RAISED, bd=3)
        frame.place(row=3, row_span=6, col=1, col_span=3, sticky="new")
        builder.root = frame.component.tk_component

        # profile data
        _create_profile_data_entry(builder, text="First name:", name="first_name", row=0)
        _create_profile_data_entry(builder, text="Last name:", name="last_name", row=1)
        _create_profile_data_entry(builder, text="Gender:", name="gender", row=2)
        _create_profile_data_entry(builder, text="Email address:", name="email", row=3)
        _create_profile_data_entry(builder, text="Date of Birth:", name="dob", row=4)
        button = builder.create(
            "button2",
            name="edit_user_data",
            text="Confirm changes",
            command=callbacks.edit_user_data,
            bd=3,
        )
        button.place(row=5, col=1, col_span=2, sticky="nse")

        # password change
        builder.root = window
        frame = builder.create("frame", relief=tk.RAISED, bd=3)
        frame.place(row=10, col=1, col_span=3, sticky="nsew")
        builder.root = frame.component.tk_component

        button = builder.create(
            "button",
            text="Change password",
            name="password_change_frame",
            command=callbacks.show_password_change_frame,
            bd=3,
        )
        button.place(row=0, col=2, sticky="w")

        frame = builder.create("frame", name="password_change", relief=tk.RAISED, bd=0)
        frame.place(row=0, row_span=3, col=0, col_span=3)
        builder.root = frame.component.tk_component
        builder.view.hide_components("password_change_frame")

        # password
        builder.create("label", text="*Password").place(row=0, col=0)
        builder.create("entry", name="pw", textvariable=tk.StringVar(), show="*").place(
            row=0, col=1, sticky="we"
        )

        # confirm password
        builder.create("label", text="*Confirm").place(row=1, col=0)
        builder.create("entry", name="confirm_pw", textvariable=tk.StringVar(), show="*").place(
            row=1, col=1, sticky="we"
        )

        button = builder.create(
            "button2",
            text="Confirm password change",
            command=callbacks.edit_user_password,
            bd=3,
        )
        button.place(row=2, col=1, sticky="e")

        return builder.view

    def store_user_data(self, user_data):
        """Stores the passed user data in the user data entries"""
        for name, value in zip(self.user_data_entries, user_data):
            self[name].set_var(value)

    def get_user_data(self):
        """Returns a UserSignUpData object containing the data in the entries"""
        return user.UserSignUpData(*(self[e].get_var() for e in self.user_data_entries))

    @property
    def user_data_entries(self) -> List[str]:
        """Getter for user_data_entries, returns list of data entries in the profile view"""
        entry_names = ["first_name", "last_name", "gender", "dob", "email"]
        return [f"{name}_entry" for name in entry_names] + ["date_joined_data_label"]


def _create_profile_data_entry(
    builder: components.Builder, text: str, name: str, row: int
) -> None:
    """Creates a labelled entry + edit button"""
    builder.create("label", text=text).place(row=row, col=0, sticky="w")

    entry = builder.create("entry", name=name, textvariable=tk.StringVar())
    entry.place(row=row, col=1, sticky="we")
    entry.component.config(state="disabled")

    callback = functools.partial(callbacks.activate_profile_entry, entry.component.name)
    button = builder.create("button", text="Edit", command=callback, bd=3)
    button.place(row=row, col=2, sticky="e")
