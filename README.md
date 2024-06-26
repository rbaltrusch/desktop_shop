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

### Custom database generation

The database generation can be customized with the `python -m desktop.database.database generate` CLI:

```
usage: database.py [-h] [--name NAME] [--fast] [--minimal] [--transactions TRANSACTIONS] [--users USERS] [--products PRODUCTS] {generate}

Database generation interface

positional arguments:
  {generate}            database action to be performed

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           The name of the database
  --fast                reduces number of password hashing operations
  --minimal             reduces size of all tables to 1
  --transactions TRANSACTIONS
                        pass number of transactions to be added to database
  --users USERS         pass number of users to be added to database
  --products PRODUCTS   pass number of products to be added to database
```

To display the CLI doc above, run `python -m desktop.database.database -h`.

## ⚠️ State of the repository ⚠️

This repository is unlikely to receive new features in the future, although maintenance and small fixes will still be done.

This means that some features that are missing now will stay missing (but feel free to submit a pull request to add them!), and non-optimal aspects of the codebase or the application are unlikely to get fixed. Some of these include:
- No admin panel
- A user cannot see the transactions that he has placed in the past
- The application asking for gender is a violation of the EU GDPR, as this user data is not required with the application as is (the same potentially applies to collecting date of birth).
- The interface to the database is not ideal, as typing is missing for the most part, it is somewhat internally inconsistent, and is using lists or tuples instead of objects.

## Contributions

To contribute to this repository, please read the [contribution guidelines](https://github.com/rbaltrusch/desktop_shop/blob/master/CONTRIBUTING.md).

## Python

Written in Python 3.8.3.

## License

This repository is open-source software available under the [MIT License](https://github.com/rbaltrusch/desktop_shop/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
