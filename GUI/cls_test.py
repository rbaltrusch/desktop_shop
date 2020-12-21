# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:54:19 2020

@author: Korean_Crimson
"""
import tkinter as tk

class Tk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry = None

    def mainloop(self):
        super().mainloop()
        print(self.entry.get())

window = Tk()
window.entry = tk.Entry(width=50)
window.entry.pack()
window.mainloop()