# desktop_shop
Desktop mock shop application interfacing with a generated database of customers, products and transactions (Python / SQLite3).

Considerations/Limitations/Problems:

	no cache: shopping cart gets discarded when session is disconnected
	if duplicate products in orders, cost of the order is not properly calculated
	no networking/server (to reduce extra complexity)

To try out the graphical database application, simply install all the required packages (specified in requirements.txt) and run gui.py.

Written in Python 3.8.3