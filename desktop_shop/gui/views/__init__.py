# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:47:28 2021

@author: richa
"""
from typing import Dict
from typing import Type

from desktop_shop.gui import components

from . import checkout
from . import home
from . import login
from . import main_menu
from . import profile
from . import register


class View(components.View):
    """View Protocol interface"""

    @classmethod
    def create(cls, window: components.Tk, builder: components.Builder) -> components.View:
        """Creates the View"""

views: Dict[str, Type[View]] = {
    "checkout": checkout.View,
    "home": home.View,
    "login": login.View,
    "main_menu": main_menu.View,
    "profile": profile.View,
    "register": register.View,
}
