# -*- coding: utf-8 -*-
"""Tests for the desktop_shop.datagen.data module"""

import os
import shutil
from typing import Union

import pytest

from desktop_shop.datagen import data


class Row:
    def __init__(self, *fields: str):
        self.fields = fields

    def __str__(self):
        return "<tr>" + "".join(f"<td>{x}</td>" for x in self.fields) + "</tr>"


class Table:
    def __init__(self, *rows: Row):
        self.rows = rows

    def __str__(self):
        return "<table>" + "".join(map(str, self.rows)) + "</table>"


class MockPage:
    def __init__(self, *body_elements: Union[Table, Row]):
        self.body_elements = body_elements

    def get(self, *_):
        """For requests mock"""
        return self

    def html(self) -> str:
        """For wikipedia mock"""
        return self.content

    @property
    def content(self) -> str:
        """For requests mock"""
        return f"<html><body>{''.join(map(str, self.body_elements))}</body></html>"


class MockWikipedia:
    def __init__(self, page):
        self._page = page

    def page(self, _):
        return self._page


def _remove_cache():
    folder = ".html_cache"
    if os.path.isdir(folder):
        shutil.rmtree(folder)


@pytest.mark.parametrize(
    "page, expected",
    [
        (MockPage(Table()), {}),
        (
            MockPage(Table(*[Row(*[str(x + y * 5) for x in range(5)]) for y in range(5)])),
            {"11": "m", "13": "f", "16": "m", "18": "f"},
        ),
    ],
)
def test_fetch_first_names(page, expected, monkeypatch):
    _remove_cache()
    monkeypatch.setattr(data, "requests", page)
    assert data.fetch_first_names() == expected


@pytest.mark.parametrize(
    "page, expected",
    [
        (MockPage(), []),
        (
            MockPage(
                Table(
                    Row(),
                    Row("a", "b"),
                    Row("1", "2", "3"),
                    Row("abc", "def", "gef"),
                    Row("something", "def", "hello"),
                    Row("something", "deffo", "hello"),
                )
            ),
            ["def", "deffo"],
        ),
    ],
)
def test_fetch_last_names(page, expected, monkeypatch):
    _remove_cache()
    monkeypatch.setattr(data, "wikipedia", MockWikipedia(page))
    assert sorted(data.fetch_last_names()) == expected


def test_fetch_with_caching(monkeypatch):
    """Expecting the same result in both cases due to caching"""
    _remove_cache()  # remove initial cache
    expected = ["def"]
    page = MockPage(Table(Row("abc", "def", "gef")))
    monkeypatch.setattr(data, "wikipedia", MockWikipedia(page))
    assert sorted(data.fetch_last_names()) == expected

    # expect same result with different page due to caching
    MockPage(Table(Row("some", "thing", "different")))
    monkeypatch.setattr(data, "wikipedia", MockWikipedia(page))
    assert sorted(data.fetch_last_names()) == expected


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ((2000, 1, 1), (2000, 1, 5), "2000-01-04"),
        ((2005, 5, 13), (2016, 7, 28), "2016-07-27"),
    ],
)
def test_get_random_date(start, end, expected, monkeypatch):
    class MockRandom:
        @staticmethod
        def randrange(x: int) -> int:
            return x - 1

    monkeypatch.setattr(data, "random", MockRandom)
    assert data.get_random_date(start, end) == expected


@pytest.mark.parametrize(
    "start, end",
    [
        ((2000, 1, 1), (1999, 12, 31)),
        ((2000, 12, 1), (2000, 13, 1)),
    ],
)
def test_get_random_date_fail(start, end):
    with pytest.raises(ValueError):
        data.get_random_date(start, end)
