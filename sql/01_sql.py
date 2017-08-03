""" 데이터베이스 및 table 생성 """

import sqlite3

conn = sqlite3.connect("new.db")

cursor = conn.cursor()

cursor.execute("CREATE TABLE population (city TEXT, state TEXT, population INT)")

conn.close()