import os
import tempfile
import json

from flask import Flask, request, redirect, url_for, send_from_directory
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)

@app.route('/mongo/users/put', methods=['PUT'])
def mongo_sign_up():
    try:
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        client = MongoClient()
        db = client.test_db
        db.users.insert_one(
        {
        "email": email.lower(),
        "password": password,
        "name": name,
        "surname": surname
        })
        return "gud"
    except Exception as e:
        return "error: %s" % (e)


@app.route('/mongo/users/get', methods=['GET'])
def mongo_get_users():
    try:
        client = MongoClient()
        db = client.test_db
        users = db.users
        result = []
        for user in users.find():
            result.append(
            {
            'email': user['email'],
            'password': user['password'],
            'name': user['name'],
            'surname': user['surname']
            })
        return json.dumps(result)
    except Exception as e:
        return "error: %s" % (e)


@app.route('/mongo/login', methods=['POST'])
def mongo_login():
    email = request.form['email']
    password = request.form['password']
    print('email: %s, password: %s' % (email, password))
    try:
        client = MongoClient()
        db = client.test_db
        user = db.users.find_one({'email': email.lower()})
        if user and user['password'] == password:
            result = {
            'resultCode': '1',
            'email': user['email'],
            'name': user['name'],
            'surname': user['surname']
            }
        else:
            result = {
            'resultCode': '0',
            }

        print result
        return json.dumps(result)

    except Exception as e:
        return "error: %s" % (e)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print 'No file part'
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = {
                'resultCode': '1'
                }
        if result is None:
            result = {
            'resultCode': '0'
            }

        print result
        return json.dumps(result)

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    filename = secure_filename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
