import sqlite3

with sqlite3.connect("newnum.db") as connection:
    c = connection.cursor()

    prompt = """
    Select the operation that you want to perform [1-5]:
    1. Average
    2. Max 
    3. Min 
    4. Sum 
    5.Exit 
    """

    while True:
        x = input(prompt)

        if x in set(["1", "2", "3", "4"]):
            operation = {1:"avg", 2:"max", 3:"min", 4:"sum"}[int(x)]

            c.execute("SELECT {}(num) from numbers".format(operation))

            get = c.fetchone()

            print(operation + " : %f" % get[0])
        elif x=="5":
            print("Exit")
            break

