import sqlite3

conn = sqlite3.connect('db/database.db')
curr = conn.cursor()
with open('schema.sql') as f:
    curr.executescript(f.read())

conn.commit()
conn.close()
