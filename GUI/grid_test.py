# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:52:27 2020

@author: Korean_Crimson
"""

import tkinter as tk

window = tk.Tk()

for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)
    for j in range(3):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, sticky="nsew")
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        #label.pack()
        label.pack(padx=5, pady=5) #give some whitespace padding

window.mainloop()