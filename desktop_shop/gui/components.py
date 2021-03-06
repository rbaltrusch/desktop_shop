# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:53:11 2021

@author: Korean_Crimson
"""

import tkinter as tk

class Tk(tk.Tk):
    '''Wrapper around tk.Tk class with easier rowconfigure and columnconfigure functionality'''
    def __init__(self):
        super().__init__()
        self.col_num = 0
        self.row_num = 0

    def add_row(self, minsize, weight=1):
        '''Wraps around tk.Tk.rowconfigure'''
        self.rowconfigure(self.row_num, minsize=minsize, weight=weight)
        self.row_num += 1

    def add_col(self, minsize, weight=1):
        '''Wraps around tk.Tk.columnconfigure'''
        self.columnconfigure(self.col_num, minsize=minsize, weight=weight)
        self.col_num += 1

class Gui:
    '''Class to contain all tk widgets, tk Vars and other data related to the gui'''
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
        '''Wraps around tk.Tk.mainloop'''
        self.window.mainloop()

    def pack_all(self):
        '''Places all active views on the gui by calling pack'''
        for view in self.views_dict.values():
            if view.active:
                view.pack()
            else:
                view.unpack()

    def deactivate_all(self):
        '''Deactivates all views'''
        for view in self.views_dict.values():
            view.deactivate()

    def switch_to(self, *keys):
        '''Switches to a particular view (deactivates all other views)'''
        self.deactivate_all()
        for key in keys:
            self.views_dict[key].activate()
        self.pack_all()

class View():
    '''View class that acts as a container of a number of related Component objects'''
    def __init__(self):
        self.active = False
        self._components = {}
        self._frame_components = {}

    def get(self, component_name):
        '''Returns the component identified by the passed name'''
        return self._all_components[component_name]

    def get_frames(self):
        '''Returns all Components that are marked as frames'''
        return self._frame_components.values()

    def clear(self):
        '''Clears the current view by unpacking all components and clearing all
        component dicts (uninitialises the entire view).
        '''
        self.unpack()
        self._components = {}
        self._frame_components = {}

    def activate(self):
        '''Activates the current view (when the Gui object next calls pack on it,
        this View will show when active)
        '''
        self.active = True

    def deactivate(self):
        '''Deactivates the current view (when the Gui object next calls pack on it,
        this View will not show when deactive)
        '''
        self.active = False

    def add_component(self, component, name):
        '''Adds the passed Component under the specified name and stores it in the view'''
        self._components[name] = component

    def add_frame_component(self, component, name):
        '''Adds the passed Component under the specified name and stores it in the view, as
        a component of type frame
        '''
        self._frame_components[name] = component

    def pack(self):
        '''Calls gridpack on all components in the view (frames first)'''
        for component in self._all_components.values():
            component.gridpack()

    def repack(self):
        '''Unpacks, then repacks the view'''
        self.unpack()
        self.pack()

    def unpack(self):
        '''Calls unpack for all components in the view (frames first)'''
        for component in self._all_components.values():
            component.unpack()

    def hide_component(self, component_name):
        '''Hides a particular component'''
        self._all_components[component_name].hide()

    def unhide_component(self, component_name):
        '''Unhides a particular component'''
        component = self._all_components[component_name]
        component.unhide()
        component.gridpack()

    @property
    def _all_components(self):
        return {**self._components, **self._frame_components}

#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-arguments
class Component():
    '''Wrapper class around tk widgets, that stores all data usually required when
    calling .grid(). Using this class makes it possible to repeatedly call grid()
    and grid_forget() for variable gui layouts without passing the arguments repeatedly
    '''
    def __init__(self, tk_component, row=0, column=0, sticky='n', padx=0, pady=0,
                 column_span=1, row_span=1, var=None):
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
        '''Hides the component and calls unpack'''
        self.hidden = True
        self.unpack()

    def unhide(self):
        '''Unhides the component'''
        self.hidden = False

    def gridpack(self):
        '''calls .grid on the tk_component if it is not hidden'''
        if not self.hidden:
            self.tk_component.grid(row=self.row,
                                   column=self.column,
                                   sticky=self.sticky,
                                   padx=self.padx,
                                   pady=self.padx,
                                   rowspan=self.row_span,
                                   columnspan=self.column_span
                                   )

    def unpack(self):
        '''calls .grid_forget on the tk_component'''
        self.tk_component.grid_forget()

    def get(self):
        '''calls .get on the tk_component'''
        return self.tk_component.get()

    def get_var(self):
        '''calls .get on the stored tk Var'''
        return self.var.get() if self.var else None

    def set_var(self, value):
        '''calls .set on the stored tk Var'''
        if self.var:
            self.var.set(value)

    def config(self, *args, **kwargs):
        '''calls .config on the tk_component'''
        self.tk_component.config(*args, **kwargs)
