# desktop_shop
Desktop mock shop application interfacing with a generated database of customers, products and transactions (Python / SQLite3).

Considerations/Limitations/Problems:

	no cache: shopping cart gets discarded when session is disconnected
	if duplicate products in orders, cost of the order is not properly calculated
	no networking/server (to reduce extra complexity)
