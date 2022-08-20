# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:47:28 2021

@author: richa
"""
from typing import Dict, Type

from desktop_shop.gui import components
from desktop_shop.gui.views import checkout, home, login, main_menu, profile, register

views: Dict[str, Type[components.View]] = {
    "checkout": checkout.View,
    "home": home.View,
    "login": login.View,
    "main_menu": main_menu.View,
    "profile": profile.View,
    "register": register.View,
}
