import sqlite3

# Buat atau terhubung ke database
conn = sqlite3.connect('login.db')
cursor = conn.cursor()

# Buat tabel pengguna
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Simpan perubahan
conn.commit()

# Tutup koneksi ke database
conn.close()

