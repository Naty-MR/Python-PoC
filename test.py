from flask import Flask
from flask import request
import json
app = Flask(__name__)
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password_root'
app.config['MYSQL_DATABASE_DB'] = 'test_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = '%s' AND password = '%s'" % (email, password))
        data = cursor.fetchall()
        cursor.close()
        for user in data:
            row_headers=[x[0] for x in cursor.description]
            json_data = (dict(zip(row_headers, user)))
            return json.dumps(json_data)

        return "Credenciales incorrectas"
    except Exception as e:
        return "error: %s" % (e)


@app.route('/users/put', methods=['PUT'])
def sign_up():
    try:
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("INSERT INTO users (email, password, name, surname) VALUES ('%s', '%s', '%s', '%s')" % (email, password, name, surname))
        cursor.close()
        conn.commit()
        return "gud"
    except Exception as e:
        return "error: %s" % (e)


@app.route('/users/get', methods=['GET'])
def get_users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        row_headers=[x[0] for x in cursor.description]
        json_data = []
        for user in data:
            json_data.append(dict(zip(row_headers, user)))

        return json.dumps(json_data)
    except Exception as e:
        return "error: %s" % (e)
