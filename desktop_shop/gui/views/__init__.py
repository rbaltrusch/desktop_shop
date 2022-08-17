# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:47:28 2021

@author: richa
"""
from typing import Dict, Type

from desktop_shop.gui import components

from . import checkout, home, login, main_menu, profile, register


class View(components.View):
    """View Protocol interface"""

    @classmethod
    def create(
        cls, window: components.Tk, builder: components.Builder
    ) -> components.View:
        """Creates the View"""


views: Dict[str, Type[View]] = {
    "checkout": checkout.View, # type: ignore
    "home": home.View, # type: ignore
    "login": login.View, # type: ignore
    "main_menu": main_menu.View, # type: ignore
    "profile": profile.View, # type: ignore
    "register": register.View, # type: ignore
}
