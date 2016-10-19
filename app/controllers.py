from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_pymongo import PyMongo
from flask_bcrypt import bcrypt
import datetime

app = Flask(__name__)

app.config.from_object('config')

mongo = PyMongo(app)


@app.route('/')
def index():
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
            return redirect(url_for('all_blogs',username=username))
        flash("Username Already Exists!!")
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
                return redirect(url_for('all_blogs', username=username))
        flash("Invalid credentials!! Check username/password combination")
    return render_template('login.html')


@app.route('/dashboard/<username>')
# def dashboard(username):
#     return render_template('dashboard.html', username=username)

def all_blogs(username):
    users = mongo.db.Users
    blogs = mongo.db.Blogs
    active_user = users.find_one({'Username' : username})
    user_blogs = blogs.find({'Author_id' : active_user['_id']})
    # blog_list = ""
    # for x in user_blogs:
    #     blog_list += x['Title']
    return render_template('dashboard.html', username=username, user_blogs=user_blogs)


@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)


@app.route('/save_user/<username>', methods=['POST', 'GET'])
def save_user(username):
    if request.method == 'POST':
        users = mongo.db.Users
        password = request.form['Password']
        confirm_password = request.form['ConfirmPassword']
        if password == confirm_password:
            valid_user = users.find_one({'Username': username})
            valid_user['Password'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users.save(valid_user)
            flash("Changes Saved")
            return redirect(url_for('profile', username=username))
        flash("Invalid credentials!! Kindly confirm Password")
    return redirect(url_for('profile', username=username))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#
# @app.route('/dashboard/<username>')
#
#
#     # return render_template('blogs.html', username=username, blog_list={{blog_list}})


@app.route('/add_blog/Author:<username>',methods=['POST','GET'])
def add_blog(username):
    if request.method == 'POST':
        users = mongo.db.Users
        blogs = mongo.db.Blogs
        new_blogTitle = request.form['Blog_Title']
        new_blogContent= request.form['Blog_Content']
        author= users.find_one({'Username' : username})

        if new_blogTitle is not None and new_blogContent is not None:

            blogs.insert({'Title': new_blogTitle, 'Content': new_blogContent, \
                        'Author_id' : author['_id'], 'Date' : datetime.datetime.utcnow()})
            flash("Congratulations! You have a new blog")
            return redirect(url_for('all_blogs', username=username))
        flash("Blog must have a title and content")

    return render_template('add_blog.html',username=username)


@app.route('/blog/<int:blog_id>',methods=['POST','GET'])
def blog(blog_id):
    blogs = mongo.db.Blogs
    active_blog = blogs.find_one({'_id' : blog_id})
    id = active_blog['_id']
    title = active_blog['Title']
    content = active_blog['Content']
    date_published = active_blog['Date']
    author = session
    return render_template('blog.html', id=id, title=title, content=content, \
                           date_published=date_published, author=author)

