import sqlite3

with sqlite3.connect("cars.db") as connection:

    c = connection.cursor()
    c.execute("INSERT INTO inventory VALUES('Ford', 'Focus', 10)")
    c.execute("INSERT INTO inventory VALUES('Honda', 'Civic', 11)")
    c.execute("INSERT INTO inventory VALUES('Ford', 'Ranger', 12)")
    c.execute("INSERT INTO inventory VALUES('Honda', 'Accord', 13)")
    c.execute("INSERT INTO inventory VALUES('Ford', 'Avenger', 14)")

    c.execute("UPDATE inventory SET quantity = 15 WHERE model='Focus'")
    c.execute("UPDATE inventory SET quantity = 16 WHERE model='Civic'")

    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    for row in rows:
        print(row[0], row[1], row[2])

    