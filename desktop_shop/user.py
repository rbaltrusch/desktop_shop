# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 23:08:31 2021

@author: richa
"""

from dataclasses import dataclass

@dataclass    
class UserData:
    first_name: str = ''
    last_name: str = ''
    gender: str = ''
    join_date: str = ''
    user_email: str = ''
    dob: str = ''

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
