from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime
import os

app = Flask(__name__)

# Creacion de la base de datos, tablas y campos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Creating User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(10), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Creating post table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(100), unique=False)    
    date = db.Column(db.DateTime, unique=False)

    def __init__(self, address, description, date):
        self.address = address
        self.description = description
        self.date = date


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'address', 'description', 'date')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


# API for users login
@app.route('/home')
def home():
    return render_template("home.html")

# @app.route('/login', methods=["GET","POST"])
# def login():
#     error = ''
#     users = ["edwin", "angela", "tyson", "joe", "jess", "jacob", "ryan", "kent"]
#     flag = False

#     try:	
#         if request.method == "POST":		
#             username = request.form['username']
#             password = request.form['password']  

#             for user in users:
#                 if username == user:
#                     flag = True
#                     break

#             if flag and password == "1234":                                   
#                 return redirect(url_for('home'))				
#             else:
#                 error = "Invalid credentials. Try Again."

#         return render_template("login.html", error = error)

#     except Exception as e:
#         return render_template("login.html", error = error)  

# ----------------------------------------------------------------------
# API's for users request

# Endpoint to create a new comment
@app.route('/login', methods=["POST"])
def add_login():  
    if request.method == "POST":		
        username = request.form['username'] 
        password = request.form['password'] 
        new_user = User(username, password)

        db.session.add(new_user)
        db.session.commit()    

        user_1 = User.query.get(new_user.id)
    return user_schema.jsonify(user_1)          

    # return render_template("post.html")  


if __name__ == '__main__':
    app.run(debug=True)
