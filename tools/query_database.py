# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 17:09:26 2020

@author: Korean_Crimson
"""
import sqlite3


def query_power_users(cursor):
    """get name, number of transactions, total cost of all male users that spent
    over 1000 euro and were born in 2004.
    """
    data = cursor.execute(
        """SELECT l.first_name, l.last_name, l.dob, COUNT(*), SUM(r.cost)
                          FROM users l INNER JOIN transactions r ON l.user_id = r.user_id
                          WHERE l.gender="m" AND l.dob GLOB "2004*" GROUP BY r.user_id
                          HAVING SUM(r.cost) > 1000 ORDER BY SUM(r.cost) DESC"""
    )
    for row in data:
        print(row)


def query_transactions_for_user(cursor, email):
    """Query transactions from a user by the specified email"""
    data = cursor.execute(
        """SELECT * FROM transactions WHERE user_id IN
                          (SELECT user_id FROM users WHERE email_address = ?)""",
        (email,),
    )
    for row in data:
        print(row)


def query_transactions_for_user_by_pattern(cursor, pattern):
    """Retrieve transactions for user where the last name matches the specified sqlite3 pattern.
    e.g. the pattern P%r would match Peter.
    """
    data = cursor.execute(
        """SELECT user_id FROM users
                          WHERE last_name LIKE ? ORDER BY first_name""",
        (pattern,),
    )
    data = list(data)
    if not data:
        return

    data = cursor.execute("SELECT * FROM transactions WHERE user_id IN (?)", data[0])
    for row in data:
        print(row)


def query_transaction_price(cursor, transaction_id):
    """Returns the total price of the transaction specified by the passed id"""
    data = cursor.execute(
        """SELECT SUM(price) FROM products
                          WHERE product_id in
                          (SELECT d.product_id FROM detailed_transactions d
                           INNER JOIN transactions t ON d.transaction_id = t.transaction_id
                           WHERE t.transaction_id = ?)""",
        (transaction_id,),
    )
    for row in data:
        print(row)


def list_some_users(cursor, limit=100):
    """Lists the first users in the user table, limited to the specified amount"""
    data = cursor.execute("SELECT * FROM users LIMIT ?", (limit,))
    for row in data:
        print(row)


def list_sqlite_tables(cursor):
    """Lists all the tables found the database"""
    data = cursor.execute('''SELECT name FROM sqlite_master where type="table"''')
    for row in data:
        print(row)


def list_all_sessions(cursor):
    """Lists all data in the sessions table"""
    data = cursor.execute("""SELECT * FROM sessions""")
    for row in data:
        print(row)


def list_products(cursor):
    """Lists products, descending by price"""
    data = cursor.execute("SELECT * FROM products ORDER BY price DESC")
    for row in data:
        print(row)


def list_cheapest_transactions(cursor, limit=10):
    """Lists the cheapest transactions, limited to the amount specified"""
    data = cursor.execute(
        """SELECT date, cost, user_id FROM transactions
                          ORDER BY cost ASC LIMIT ?""",
        (limit,),
    )
    for row in data:
        print(row)


def list_biggest_consumers(cursor, orders=20):
    """Lists the users that have more than the specified amount of orders"""
    data = cursor.execute(
        """SELECT user_id, COUNT(*), SUM(cost) FROM transactions
                          GROUP BY user_id HAVING COUNT(*) > ?
                          ORDER BY SUM(cost) DESC""",
        (orders,),
    )
    for row in data:
        print(row)


def main():
    """Main function"""
    with sqlite3.connect("../desktop_shop/main.db") as cursor:
        query_transactions_for_user_by_pattern(cursor, "A%r")


if __name__ == "__main__":
    main()
