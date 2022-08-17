# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 23:08:31 2021

@author: richa
"""

from dataclasses import dataclass


# pylint: disable=function-redefined
@dataclass
class UserData:
    """Stores user data"""

    first_name: str = ""
    last_name: str = ""
    gender: str = ""
    dob: str = ""  # date of birth
    email: str = ""

    def __getitem__(self, value):
        return list(self)[value]

    def __iter__(self):
        yield self.first_name
        yield self.last_name
        yield self.gender
        yield self.dob
        yield self.email

    @property
    def full_name(self) -> str:
        """Full name getter, returns first and last names joined together"""
        return f"{self.first_name} {self.last_name}"

    @property  # type: ignore
    def first_name(self) -> str:
        """First name getter, returns capitalized first name"""
        return self._first_name.title()

    @first_name.setter
    def first_name(self, value):
        """First name setter"""
        self._first_name: str = value

    @property  # type: ignore
    def last_name(self) -> str:
        """Last name getter, returns capitalized last name"""
        return self._last_name.title()

    @last_name.setter
    def last_name(self, value):
        """Last name setter"""
        self._last_name: str = value


@dataclass
class UserSignUpData(UserData):
    """Stores user data and join date"""

    join_date: str = ""

    def __iter__(self):
        for attr in super().__iter__():
            yield attr
        yield self.join_date
