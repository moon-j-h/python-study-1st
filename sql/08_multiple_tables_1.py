import sqlite3

with sqlite3.connect("new.db") as connection:

    c=connection.cursor()
    cities = [
        ('Boston', 'MA', 600000),
        ('Los Angeles', 'CA', 30000000),
        ('Houston', 'TX', 210000),
        ('Philadelphia', 'PA', 1500000),
        ('San Antonio', 'TX', 14000000),
        ('San Diego', 'CA', 1200000000),
        ('Jacksonville', 'FL', 800000),
        ('Indianapolis', 'IN', 80000000),
        ('Austin', 'TX', 800000),
        ('Detrioit', 'MI', 70000000)
    ]

    c.executemany('INSERT INTO population VALUES(?, ?, ?)', cities)
    c.execute('SELECT * FROM population WHERE population > 100000')

    rows = c.fetchall()

    for r in rows:
        print(r[0], r[1], r[2])