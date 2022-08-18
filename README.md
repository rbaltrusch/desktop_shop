[![Unit tests](https://github.com/rbaltrusch/desktop_shop/actions/workflows/pytest-unit-tests.yml/badge.svg)](https://github.com/rbaltrusch/desktop_shop/actions/workflows/pytest-unit-tests.yml)
[![Pylint](https://github.com/rbaltrusch/desktop_shop/actions/workflows/pylint.yml/badge.svg)](https://github.com/rbaltrusch/desktop_shop/actions/workflows/pylint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

# Desktop Shop

This is a mock shop application, running completely offline on a desktop. The graphical interface connects with a generated, local database of customers, products and transactions (Python / SQLite3). As the application runs completely offline, it does away with any networking or server complexity and showcases a bare implementation of an application interfacing with a production database.

![Screenshot of the application GUI](https://github.com/rbaltrusch/desktop_shop/blob/master/desktop_shop/gui/media/gif.gif?raw=true "Screenshot of the application GUI")


## Disclaimer

Any personal information shown in the gui or stored in the database is not related to any natural people. All information was generated automatically. Any names or other user data which coincide with real individuals are pure coincidence.

## Getting started

Run the shop application by installing the package using pip, then calling it:

    python -m pip install desktop_shop
    python -m desktop_shop

Note that the first time the package is called, it automatically generates a fresh database filled with random data. This make take a few seconds.

## Contributions

To contribute to this repository, please read the [contribution guidelines](https://github.com/rbaltrusch/desktop_shop/blob/master/CONTRIBUTING.md).

## Python

Written in Python 3.8.3.

## License

This repository is open-source software available under the [MIT License](https://github.com/rbaltrusch/desktop_shop/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
