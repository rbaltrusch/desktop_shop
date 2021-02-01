# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:53:11 2021

@author: Korean_Crimson
"""

import tkinter as tk

class Tk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.col_num = 0
        self.row_num = 0

    def add_row(self, minsize, weight=1):
        self.rowconfigure(self.row_num, minsize=minsize, weight=weight)
        self.row_num += 1

    def add_col(self, minsize, weight=1):
        self.columnconfigure(self.col_num, minsize=minsize, weight=weight)
        self.col_num += 1

class Gui:
    def __init__(self, window):
        self.window = window
        self.views_dict = {}
        self.data = {}
        self.focused_widget_name = None

    def __enter__(self):
        self.pack_all()
        return self

    def __exit__(self, *_):
        pass

    def mainloop(self):
        self.window.mainloop()

    def pack_all(self):
        for view in self.views_dict.values():
            if view.active:
                view.pack()
            else:
                view.unpack()

    def deactivate_all(self):
        for view in self.views_dict.values():
            view.deactivate()

    def switch_to(self, *keys):
        self.deactivate_all()
        for key in keys:
            self.views_dict[key].activate()
        self.pack_all()

class View():
    def __init__(self):
        self.active = False
        self._components = {}
        self._frame_components = {}

    def get(self, component_name):
        return self._all_components[component_name]

    def get_frames(self):
        return self._frame_components.values()

    def clear(self):
        self.unpack()
        self._components = {}
        self._frame_components = {}

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_component(self, component, name):
        self._components[name] = component

    def add_frame_component(self, component, name):
        self._frame_components[name] = component

    def pack(self):
        for component in self._all_components.values():
            component.gridpack()

    def repack(self):
        self.unpack()
        self.pack()

    def unpack(self):
        for component in self._all_components.values():
            component.unpack()

    def hide_component(self, component_name):
        self._all_components[component_name].hide()

    def unhide_component(self, component_name):
        component = self._all_components[component_name]
        component.unhide()
        component.gridpack()

    @property
    def _all_components(self):
        return {**self._components, **self._frame_components}
        

class Component():
    def __init__(self, tk_component, row=0, column=0, sticky='n', padx=0, pady=0, column_span=1, row_span=1, var=None):
        self.tk_component = tk_component
        self.row = row
        self.column = column
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.column_span = column_span
        self.row_span = row_span
        self.hidden = False
        self.var = var
        self.data = None

    def hide(self):
        self.hidden = True
        self.unpack()

    def unhide(self):
        self.hidden = False

    def gridpack(self):
        if not self.hidden:
            self.tk_component.grid(row=self.row, column=self.column, sticky=self.sticky, padx=self.padx, pady=self.padx, rowspan=self.row_span, columnspan=self.column_span)

    def unpack(self):
        self.tk_component.grid_forget()

    def get(self):
        return self.tk_component.get()

    def get_var(self):
        return self.var.get() if self.var else None

    def set_var(self, value):
        if self.var:
            self.var.set(value)

    def config(self, *args, **kwargs):
        self.tk_component.config(*args, **kwargs)
