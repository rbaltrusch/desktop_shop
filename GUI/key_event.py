# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 16:20:11 2020

@author: Korean_Crimson
"""

import tkinter as tk

window = tk.Tk()

def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress)

window.mainloop()