#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

setuptools.setup(
    name="desktop_shop",
    version="1.0.1",
    description="Desktop shop application",
    long_description=project_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords=["python"],
    author="Richard Baltrusch",
    url="https://github.com/rbaltrusch/desktop_shop",
    packages=setuptools.find_packages("."),
    package_dir={"": "."},
    python_requires=">=3.8",
    include_package_data=True,
    package_data={"desktop_shop": ["py.typed"]}, # for mypy
    # This is a trick to avoid duplicating dependencies between both setup.py and requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    install_requires=project_dir.joinpath("requirements.txt").read_text().split("\n"),
    zip_safe=False,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
)
