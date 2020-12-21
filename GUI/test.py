# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:16:05 2020

@author: Korean_Crimson
"""

import tkinter as tk
#from tkinter.filedialog import askopenfilename, asksaveasfilename

window = tk.Tk()
window.title('hello')
#window.resizable(width=False, height=False)


'''Label	A widget used to display text on the screen
Button	A button that can contain text and can perform an action when clicked
Entry	A text entry widget that allows only a single line of text
Text	A text entry widget that allows multiline text entry
Frame	A rectangular region used to group related widgets or provide padding between widgets
'''

'''relief for frames:
tk.FLAT: Has no border effect (the default value).
tk.SUNKEN: Creates a sunken effect.
tk.RAISED: Creates a raised effect.
tk.GROOVE: Creates a grooved border effect.
tk.RIDGE: Creates a ridged effect.
'''
frame = tk.Frame(relief=tk.RAISED)

label = tk.Label(
    text="Hello, Tkinter",
    fg="white",
    bg="black",
    width=10,
    height=10
)
#other fill options: tk.Y, tk.BOTH
#other side options: tk.TOP, tk.BOTTOM, tk.LEFT, tk.RIGHT
#expand True means that the width and height can expand?
label.pack(fill=tk.X, side=tk.BOTTOM, expand=True)

button = tk.Button(
    master=frame,
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow"
)
button.pack()

'''
Retrieving text with .get()
Deleting text with .delete()
Inserting text with .insert()
'''
entry = tk.Entry(fg="yellow", bg="blue", width=50)
entry.pack()

'''
Retrieve text with .get()
Delete text with .delete()
Insert text with .insert()
'''
text_box = tk.Text()
text_box.pack()
#text_box.get("1.0", tk.END) #get all text contents

frame.pack()

window.mainloop()
#window.destroy()