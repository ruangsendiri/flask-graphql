from flask import Flask, request, jsonify, g
from graphene import ObjectType, String, Int, Field, List
from flask_graphql import GraphQLView
import sqlite3, datetime
from graphene import Schema

app = Flask(__name__)

def check_authentication(username, password):
    conn = sqlite3.connect('masuk.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.before_request
def before_request():
    g.authenticated = False

    if request.endpoint == 'login':
        return

    auth = request.authorization
    if auth and check_authentication(auth.username, auth.password):
        g.authenticated = True
    else:
        return jsonify({'message': 'Authentication required'}), 401

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if check_authentication(username, password):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'})

@app.route('/absen', methods=['POST'])
def absen():
    if not g.authenticated:
        return jsonify({'message': 'Authentication required'}), 401

    data = request.get_json()
    employee_id = data.get('employee_id')
    timestamp = datetime.date.today()
    #timestamp = data.get('timestamp')
    #today = datetime.date.today()
    
    conn = sqlite3.connect('absen.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO absensi (employee_id, timestamp) VALUES (?, ?)", (employee_id, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Absensi berhasil'})

@app.route('/absen', methods=['GET'])
def get_absen():
    if not g.authenticated:
        return jsonify({'message': 'Authentication required'}), 401

    conn = sqlite3.connect('absen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM absensi")
    absen_data = [{'employee_id': row[1], 'timestamp': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(absen_data)

@app.route('/karyawan', methods=['GET'])
def get_karyawan():
    if not g.authenticated:
        return jsonify({'message': 'Authentication required'}), 401

    conn = sqlite3.connect('karyawan.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM karyawan")
    karyawan_data = [{'id': row[0], 'name': row[1], 'position': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(karyawan_data)

@app.route('/karyawan/<employee_id>', methods=['GET'])
def get_karyawan_detail(employee_id):
    if not g.authenticated:
        return jsonify({'message': 'Authentication required'}), 401

    conn = sqlite3.connect('karyawan.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM karyawan WHERE id = ?", (employee_id,))
    karyawan = cursor.fetchone()
    conn.close()

    if karyawan:
        return jsonify({'id': karyawan[0], 'name': karyawan[1], 'position': karyawan[2]})
    else:
        return jsonify({'message': 'Karyawan tidak ditemukan'}, 404)

# graphql
class Karyawan(ObjectType):
    id = Int()
    name = String()
    position = String()

class Absensi(ObjectType):
    id = Int()
    employee_id = Int()
    timestamp = String()

class Query(ObjectType):
    karyawan = Field(Karyawan, employee_id=Int())
    karyawan_list = List(Karyawan, name=String())
    absensi_hari_ini = List(Absensi)

    def resolve_absensi_hari_ini(self, info):
        if not g.authenticated:
            return []

        # Dapatkan tanggal hari ini
        today = datetime.date.today()

        conn = sqlite3.connect('absen.db')
        cursor = conn.cursor()

        # Ambil data absen hari ini
        cursor.execute("SELECT * FROM absensi WHERE DATE(timestamp) = ?", (today,))
        absensi_data = [Absensi(id=row[0], employee_id=row[1], timestamp=row[2]) for row in cursor.fetchall()]

        conn.close()
        return absensi_data

    def resolve_karyawan(self, info, employee_id):
        if not g.authenticated:
            return None

        conn = sqlite3.connect('karyawan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM karyawan WHERE id = ?", (employee_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Karyawan(id=row[0], name=row[1], position=row[2])
        else:
            return None

    def resolve_karyawan_list(self, info, name=None):
        if not g.authenticated:
            return []

        conn = sqlite3.connect('karyawan.db')
        cursor = conn.cursor()

        if name:
            cursor.execute("SELECT * FROM karyawan WHERE name = ?", (name,))
        else:
            cursor.execute("SELECT * FROM karyawan")
        karyawan_data = [Karyawan(id=row[0], name=row[1], position=row[2]) for row in cursor.fetchall()]
        conn.close()
        return karyawan_data

schema = Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run(debug=True)

