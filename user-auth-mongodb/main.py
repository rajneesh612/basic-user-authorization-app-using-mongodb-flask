from flask import Flask, render_template, url_for, request, session, redirect
#from flask.ext.pymongo import PyMongo
from flask_pymongo import PyMongo
import bcrypt
# Press Shift+F10 to expecute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'you are logged in as ' + session['username']
    return render_template('index.html')

@app.route('/login',methods = ['POST'])
def login():
    users=mongo.db.users
    login_user=users.find_one({'name' : request.form['username']})
    if login_user:
        if bcrypt.hashpw((request.form['pass']).encode('utf-8'),(login_user['password']))==(login_user['password']):
            session['username']=request.form['username']
            return redirect(url_for('index'))
        return 'Invalid username/password'
    return 'Invalid username/password'


    return ''

@app.route('/register', methods= ['POST','GET'])
def register():
    if request.method=='POST':
        users=mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username']= request.form['username']
            return redirect(url_for('index'))
        return 'Username already exists'
    return render_template('register.html')


    return ''



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
