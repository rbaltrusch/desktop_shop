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
    dob: str = ''
    email: str = ''
    join_date: str = ''

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __iter__(self):
        yield self.first_name
        yield self.last_name
        yield self.gender
        yield self.dob
        yield self.email
        yield self.join_date
