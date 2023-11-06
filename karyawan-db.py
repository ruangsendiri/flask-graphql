import sqlite3

conn = sqlite3.connect('karyawan.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS karyawan (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        position TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

