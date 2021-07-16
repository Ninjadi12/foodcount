import sqlite3
conn = sqlite3.connect('database.db')
print("Opened data successfully")

conn.execute('CREATE TABLE USERS (name TEXT, password TEXT)')
print("Table created successfully")
conn.close()