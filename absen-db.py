import sqlite3

conn = sqlite3.connect('absen.db')
cursor = conn.cursor()

# Buat tabel absensi
cursor.execute('''
    CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

