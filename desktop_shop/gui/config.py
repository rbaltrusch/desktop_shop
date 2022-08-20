# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:01:35 2021

@author: Korean_Crimson
"""

import tkinter as tk

# colours
FG = "#FFFFFF"
DISABLED_FG = "#EEEEEE"
BG = "#121212"
BG2 = "#242424"
BG3 = "#363636"
BG4 = "#484848"
BG5 = "#606060"
PRIM = "#3700B3"
SEC = "#A172E1"
ERR = "#CF6679"

# themes
ENTRY_THEME = {
    "fg": FG,
    "bg": BG4,
    "disabledbackground": BG5,
    "disabledforeground": DISABLED_FG,
}
FRAME_THEME = {"bg": BG2, "highlightbackground": BG3}
THEME = {**FRAME_THEME, "fg": FG}

LABEL_THEME = {"fg": FG, "bg": BG2, "highlightbackground": BG2}
BUTTON_THEME = {"fg": FG, "bg": BG3, "activebackground": BG4, "activeforeground": FG}
BUTTON_THEME2 = {
    "fg": FG,
    "bg": PRIM,
    "activebackground": BG4,
    "activeforeground": FG,
    "disabledforeground": DISABLED_FG,
}
DROPDOWN_THEME = {"fg": FG, "bg": BG2, "activebackground": BG2, "activeforeground": FG}
ERROR_THEME = {"fg": ERR, "bg": BG2}
MENU_THEME = {"relief": tk.RAISED, "bd": 3, "bg": BG2}
