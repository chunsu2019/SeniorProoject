from app import app
from flask import render_template, request, redirect, session, flash, url_for
from .firebase import *

import pymongo
import datetime

import sys

#post = {"author": "Su",
 #       "textL": "Testing mongodb",
  #      "date": datetime.datetime.utcnow()
#        }

#MongoDB
try:
    cluster = pymongo.MongoClient("mongodb+srv://new-user_su:147su0@cluster0.tfjyq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster.Health
    #collection = db["Profile"]
    #collection.insert_one(post)
except:
    e = sys.exc_info()[0]
    print(e)


@app.route("/")
def index():
    return render_template("public/login.html")

@app.route("/about")
def about():
    return "<h1>About page</h1>"

@app.route("/jinja")
def jinja():    
    my_name = "Su"
    return render_template("public/jinja.html", my_name=my_name)


@app.route("/signup")
def signup():
    return render_template("public/signup.html")

@app.route("/firebase_login", methods=["POST"])
def firebaseLogin():
    if request.method == "POST":
        req = request.form
        email = req["inputEmail"]
        password = request.form["inputPassword"]

        if login(email, password):
            session["email"] = email
            return redirect(url_for("home"))
        else:
            flash("Invalid Email or Password")
            return redirect(url_for("index"))

@app.route("/firebase_signup", methods=["POST"])
def firebaseSignup():
    if request.method == "POST":
        req = request.form
        email = req["inputEmail"]
        password = request.form["inputPassword"]
        
        if createAccount(email, password):
            session["email"] = email
            login(email, password)
            return redirect(url_for("home"))
        else:
            flash("The email address you have entered is already registered")
            return redirect(url_for("signup"))

@app.route("/firebase_logout")
def firebaseLogout():
    logout()
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if isLoggedIn():
        active = "home"
        return render_template("public/home.html", active=active)
    else:
        return redirect(url_for("index"))
    

@app.route("/dashboard")
def dashboard():
    if isLoggedIn():
        active = "dashboard"
        return render_template("public/dashboard.html", active=active)
    else:
        return redirect(url_for("index"))

@app.route("/details")
def details():
    if isLoggedIn():
        active = "details"
        return render_template("public/details.html", active=active)
    else:
        return redirect(url_for("index"))

@app.route("/profile")
def profile():
    if isLoggedIn():
        active = "profile"
        collection = db["Profile"]
        data = collection.find_one({"_id": getUID()})
        return render_template("public/profile.html", active=active, data=data)
    else:
        return redirect(url_for("index"))


@app.route("/write", methods=["POST"])
def write():
    if (request.form["feet"] != ""):
        collection = db["Profile"]
        
        form0 = {"_id": getUID(),
                 "feet": request.form["feet"],
                 "inches": request.form["inches"],
                 "weight": request.form["weight"],
                 "age": request.form["age"]
                 }
        
        collection.update_one({"_id": getUID()},
                              {"$set":form0},
                              upsert=True
        )
        
    elif (request.form["reading"]!=""):
        collection = db["Blood_Pressure"]
        
        form1 = {"_id": getUID(),
                 "date": request.form["date"],
                 "reading": request.form["reading"]
                 }
        collection.insert_one(form1)
    
    else: 
        print("ERROR")
        
    print("not called")
    
    return render_template("public/home.html")