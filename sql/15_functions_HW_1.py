import sqlite3

with sqlite3.connect("cars.db") as connection:
    c = connection.cursor()

    c.execute("SELECT DISTINCT make, model FROM inventory")

    rows = c.fetchall()
    print(rows)
    for r in rows:
        print(r[0], r[1])
        c.execute("SELECT count(order_date) FROM orders WHERE model=? AND make=?", (r[1], r[0]))
        count = c.fetchone()
        print(count[0])

