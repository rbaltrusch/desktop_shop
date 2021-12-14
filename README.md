[![Python Package using Conda](https://github.com/rbaltrusch/desktop_shop/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/rbaltrusch/desktop_shop/actions/workflows/python-package-conda.yml)
[![Pylint](https://github.com/rbaltrusch/desktop_shop/actions/workflows/pylint.yml/badge.svg)](https://github.com/rbaltrusch/desktop_shop/actions/workflows/pylint.yml)

# Desktop Shop

This is a mock shop application, running completely offline on a desktop. The graphical interface connects with a generated, local database of customers, products and transactions (Python / SQLite3). As the application runs completely offline, it does away with any networking or server complexity and showcases a bare implementation of an application interfacing with a production database.

![Screenshot of the application GUI](desktop_shop/gui/media/gif.gif?raw=true "Screenshot of the application GUI")


## Disclaimer

Any personal information shown in the gui or stored in the database is not related to any natural people. All information was generated automatically. Any names or other user data which coincide with real individuals are pure coincidence.

## Getting started

To get a copy of this repository, simply open up git bash in an empty folder and use the command:

    $ git clone https://github.com/rbaltrusch/desktop_shop

To install all python dependencies, run the following in your command line:

    python -m pip install -r requirements.txt

Run the shop application by generating the random database (this can take a few seconds) and calling the main.py file:

    cd desktop_shop
    python database.py generate --fast
    python main.py

To run tests, change into the tests directory and run run_tests:

    cd tests
    python run_tests.py --all

## Python

Written in Python 3.8.3.

## License

This repository is open-source software available under the [MIT License](https://github.com/rbaltrusch/desktop_shop/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
