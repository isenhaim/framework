import sqlite3

connector = sqlite3.connect('db.sqlite')
cursor = connector.cursor()

with open('db.sql', 'r') as file:
    script = file.read()


cursor.executescript(script)
cursor.close()
