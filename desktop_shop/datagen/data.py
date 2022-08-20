# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 17:29:20 2020

@author: Korean_Crimson
"""

import datetime
import random
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
import requests  # type: ignore
import wikipedia

DateTuple = Tuple[int, int, int]


def fetch_first_names() -> Dict[str, str]:
    """fetches first names from the web and returns them as a dict in the
    format first_name: gender
    """
    page = requests.get("https://www.ssa.gov/oact/babynames/decades/century.html")
    soup = BeautifulSoup(page.content, "html.parser")
    first_names = {}
    for row in soup.find("table").select("tr")[2:-1]:
        data = [data.get_text() for data in row.select("td")]
        _, male, _, female, _ = data
        first_names[male] = "m"
        first_names[female] = "f"
    return first_names


def fetch_last_names() -> List[str]:
    """fetches last names from the web and returns them in a list"""
    wiki = wikipedia.page("List_of_most_common_surnames_in_Europe")
    soup = BeautifulSoup(wiki.html(), "html.parser")

    last_names = set()
    for table in soup.find_all("table"):
        for row in table.select("tr"):
            data = [data.get_text() for data in row.select("td")]
            if len(data) == 3:
                _, last_name, _ = data
                if last_name.isalpha():
                    last_names.add(last_name)
    return list(last_names)


def get_random_date(start: DateTuple, end: DateTuple) -> str:
    """start and end each need to be a list/tuple of length 3 (Y, M, D)"""
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    time_diff = datetime.timedelta(days=random_number_of_days)
    random_date = start_date + time_diff
    return random_date.strftime("%Y-%m-%d")
