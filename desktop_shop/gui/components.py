# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:53:11 2021

@author: Korean_Crimson
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
import tkinter as tk
from typing import Any, Callable, Dict, Iterable, List, Optional, Type, Union
import uuid

Root = Union[tk.Tk, tk.Widget]


class Tk(tk.Tk):
    """Wrapper around tk.Tk class with easier rowconfigure and columnconfigure functionality"""

    def __init__(self):
        super().__init__()
        self.col_num: int = 0
        self.row_num: int = 0

    def add_row(self, minsize: int, weight: int = 1) -> None:
        """Wraps around tk.Tk.rowconfigure"""
        self.rowconfigure(self.row_num, minsize=minsize, weight=weight)
        self.row_num += 1

    def add_col(self, minsize: int, weight: int = 1) -> None:
        """Wraps around tk.Tk.columnconfigure"""
        self.columnconfigure(self.col_num, minsize=minsize, weight=weight)
        self.col_num += 1


@dataclass
class Gui:
    """Class to contain all tk widgets, tk Vars and other data related to the gui"""

    window: Tk
    views_dict: Dict[str, View] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.builder: Optional[Builder] = None

    def __enter__(self):
        self.pack_all()
        return self

    def __exit__(self, *_):
        pass

    def __getitem__(self, key: str) -> Optional[View]:
        return self.views_dict.get(key)

    def mainloop(self) -> None:
        """Wraps around tk.Tk.mainloop"""
        self.window.mainloop()

    def pack_all(self) -> None:
        """Places all active views on the gui by calling pack"""
        for view in self.views_dict.values():
            if view.active:
                view.pack()
            else:
                view.unpack()

    def deactivate_all(self) -> None:
        """Deactivates all views"""
        for view in self.views_dict.values():
            view.deactivate()

    def switch_to(self, *keys: str) -> None:
        """Switches to a particular view (deactivates all other views)"""
        self.deactivate_all()
        for key in keys:
            self.views_dict[key].activate()
        self.pack_all()


class View:
    """View class that acts as a container of a number of related Component objects"""

    def __init__(self):
        self.active = False
        self._components: Dict[str, Component] = {}
        self._entries = {}
        self._frame_components: Dict[str, Component] = {}

    def __getitem__(self, component_name):
        """Returns the component identified by the passed name"""
        return self._all_components[component_name]

    @classmethod
    def create(cls, window: Tk, builder: Builder):  # pylint: disable=unused-argument
        """Initialises an empty view in the specified window using the specified builder"""
        return cls()

    def get_frames(self) -> Iterable[Component]:
        """Returns all Components that are marked as frames"""
        return self._frame_components.values()

    def clear(self) -> None:
        """Clears the current view by unpacking all components and clearing all
        component dicts (uninitialises the entire view).
        """
        self.unpack()
        self._components = {}
        self._frame_components = {}

    def filter(self, value: str) -> List[Component]:
        """Returns components containing the passed string in their name"""
        return [c for c in self._all_components.values() if c.name is not None and value in c.name]

    def activate(self) -> None:
        """Activates the current view (when the Gui object next calls pack on it,
        this View will show when active)
        """
        self.active = True

    def deactivate(self) -> None:
        """Deactivates the current view (when the Gui object next calls pack on it,
        this View will not show when deactive)
        """
        self.active = False

    def add_component(self, component: Component, name: str) -> None:
        """Adds the passed Component under the specified name and stores it in the view"""
        self._components[name] = component

    def add_entry_component(self, component: Component, name: str) -> None:
        """Adds the passed entry component under the specified name and stores it in the view"""
        self._components[f"{name}_entry"] = component
        self._entries[name] = component

    def add_frame_component(self, component: Component, name: str) -> None:
        """Adds the passed Component under the specified name and stores it in the view, as
        a component of type frame
        """
        self._frame_components[name] = component

    def pack(self) -> None:
        """Calls gridpack on all components in the view (frames first)"""
        for component in self._all_components.values():
            component.gridpack()

    def repack(self) -> None:
        """Unpacks, then repacks the view"""
        self.unpack()
        self.pack()

    def unpack(self) -> None:
        """Calls unpack for all components in the view (frames first)"""
        for component in self._all_components.values():
            component.unpack()

    def hide_components(self, *component_names: str) -> None:
        """Hides a particular component"""
        for component_name in component_names:
            self._all_components[component_name].hide()

    def unhide_components(self, *component_names: str) -> None:
        """Unhides a particular component"""
        for component_name in component_names:
            component = self._all_components[component_name]
            component.unhide()
            component.gridpack()

    @property
    def _all_components(self) -> Dict[str, Component]:
        return {**self._components, **self._frame_components}


# pylint: disable=too-many-instance-attributes
@dataclass
class Component:
    """Wrapper class around tk widgets, that stores all data usually required when
    calling .grid(). Using this class makes it possible to repeatedly call grid()
    and grid_forget() for variable gui layouts without passing the arguments repeatedly
    """

    tk_component: tk.Widget
    row: int = 0
    col: int = 0
    sticky: str = "n"
    padx: int = 0
    pady: int = 0
    col_span: int = 1
    row_span: int = 1
    var: Any = None
    name: str = ""

    def __post_init__(self):
        self.data = None
        self.hidden = False

    def hide(self) -> None:
        """Hides the component and calls unpack"""
        self.hidden = True
        self.unpack()

    def unhide(self) -> None:
        """Unhides the component"""
        self.hidden = False

    def add_to(self, view: View) -> None:
        """Adds the component to the passed view"""
        view.add_component(self, self.name)

    def gridpack(self) -> None:
        """calls .grid on the tk_component if it is not hidden"""
        if self.hidden:
            return

        self.tk_component.grid(
            row=self.row,
            column=self.col,
            sticky=self.sticky,
            padx=self.padx,
            pady=self.padx,
            rowspan=self.row_span,
            columnspan=self.col_span,
        )

    def unpack(self) -> None:
        """calls .grid_forget on the tk_component"""
        self.tk_component.grid_forget()

    def get(self) -> Any:
        """calls .get on the tk_component"""
        return self.tk_component.get()  # type: ignore # pylint: disable=no-member

    def get_var(self) -> Any:
        """calls .get on the stored tk Var"""
        return self.var.get() if self.var else None  # type: ignore

    def set_var(self, value) -> None:
        """calls .set on the stored tk Var"""
        if self.var:
            self.var.set(value)  # type: ignore

    def config(self, *args, **kwargs) -> None:
        """calls .config on the tk_component"""
        self.tk_component.config(*args, **kwargs)  # type: ignore


class Frame(Component):
    """Frame compoenent"""

    def add_to(self, view: View) -> None:
        """Adds the frame component to the view. Overrides Component.add_to"""
        view.add_frame_component(self, self.name)


@dataclass
class ComponentPlacer:
    """Component placer class, returned from Factory.create"""

    component: Component

    def place(self, **kwargs: Any):
        """Places the component using the specified keyword arguments"""
        for key, value in kwargs.items():
            setattr(self.component, key, value)


@dataclass
class Factory:
    """Factory object, contains a method and a respective component class,
    as well as creation arguments and keyword arguments.
    """

    method: Callable[..., tk.Widget]
    component: Type
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def create(self, root: Root, name: str = None, **kwargs: Any) -> ComponentPlacer:
        """Creates a new Component by calling the creation method. Returns a ComponentPlacer"""
        widget = self.method(root, *self.args, **self.kwargs, **kwargs)
        component = self.component(widget, name=name)
        return ComponentPlacer(component)


# pylint: disable=too-few-public-methods
class EntryFactory(Factory):
    """Entry factory"""

    def create(self, root: Root, name: str = None, **kwargs: Any) -> ComponentPlacer:
        """Overrides Factory.create.
        Adds an extra textvariable to the widget creation process.
        """
        component_placer = super().create(root, name, **kwargs)
        component_placer.component.var = kwargs.get("textvariable")
        return component_placer


class Builder:
    """Component builder class"""

    def __init__(self, **factory_methods: Factory):
        self.factory_methods = factory_methods
        self.view: View = None  # type: ignore
        self.root: Root = None  # type: ignore

    def register(self, method_name: str, factory: Factory) -> None:
        """Register a factory under a specified name"""
        self.factory_methods[method_name] = factory

    def create(self, method_name: str, name: str = None, **kwargs: Any) -> ComponentPlacer:
        """Creates a component (widget) by looking up the passed method_name
        from the registered factories and calling create on it.
        Passes received keyword arguments to the factory create method.
        Returns the component's ComponentPlacer.
        """
        factory = self.factory_methods[method_name]

        method_name_ = re.sub("[0-9]+", "", method_name)
        name = f"{name}_{method_name_}" if name is not None else str(uuid.uuid4())

        component_placer = factory.create(self.root, name, **kwargs)
        component_placer.component.add_to(self.view)
        return component_placer
