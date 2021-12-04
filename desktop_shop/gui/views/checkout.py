# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:03:41 2021

@author: richa
"""

from gui import components

class View(components.View):
    @classmethod
    def create(cls, _):
        '''Initialises an empty checkout view.
    
        Currently, all checkout view contents are dynamically generated in the function
        init_checkout_data_in_checkout_view
        '''
        return cls()
