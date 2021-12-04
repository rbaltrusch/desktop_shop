# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:05:23 2021

@author: richa
"""

from gui import components

class View(components.View):
    @classmethod
    def create(cls, _):
        '''Initialises an empty home view.
    
        Currently, all home view contents are dynamically generated in the function
        init_product_data_in_home_view
        '''
        return cls()
