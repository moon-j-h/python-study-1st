import sqlite3

with sqlite3.connect("cars.db") as connection:
    c = connection.cursor()

    c.execute("""SELECT inventory.make, inventory.model, inventory.quantity, orders.order_date
    FROM inventory, orders
    WHERE inventory.model=orders.model AND inventory.make=orders.make
    ORDER BY inventory.make ASC, inventory.model ASC, orders.order_date ASC""")


    rows = c.fetchall()

    for row in rows:
        print(row[0], row[1], row[2], row[3])