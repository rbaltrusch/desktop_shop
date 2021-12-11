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

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __getitem__(self, value):
        return list(self)[value]

    def __iter__(self):
        yield self.first_name
        yield self.last_name
        yield self.gender
        yield self.dob
        yield self.email

    def __init__(self, first_name, last_name, gender, dob, email):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.gender = gender
        self.dob = dob
        self.email = email


@dataclass
class UserSignUpData(UserData):
    join_date: str = ''

    def __iter__(self):
        for attr in super().__iter__():
            yield attr
        yield self.join_date

    def __init__(self, first_name="", last_name="", gender="", dob="", email="", join_date=""):
        super().__init__(first_name, last_name, gender, dob, email)
        self.join_date = join_date
