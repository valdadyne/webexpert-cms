from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt,bcrypt

app = Flask(__name__)

app.config.from_object('config')

mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.Users
        username = request.form['Username']
        password = request.form['Password']
        existing_user = users.find_one({'Username': username})
        if existing_user is None:
            hasspwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users.insert({'Username': username, 'Password': hasspwd})
            session['username']= username
            return redirect(url_for('dashboard',username=username))
        return flash("Username Already Exists!!")
    return render_template('register.html')


@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.Users
        username = request.form['Username']
        password = request.form['Password']
        valid_user = users.find_one({'Username' : username})
        if valid_user:
            if bcrypt.hashpw(password.encode('utf-8'),valid_user['Password'].encode('utf-8')) == valid_user['Password'].encode('utf-8'):
                session['username']= username
                return redirect(url_for('dashboard',username=username))
        return flash("Invalid credentials!! Check username/password combination")
    return render_template('login.html')


@app.route('/dashboard/<username>')
def dashboard(username):
    return""