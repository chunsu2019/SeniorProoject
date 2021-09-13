from app import app
from flask import render_template, request, redirect, session, flash, url_for
from .firebase import *
import base64
from werkzeug.utils import secure_filename
import os
import requests
import json
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
            
            collection =  db["Profile"]
            profileData = collection.find_one({"_id": getUID()})
            
            if profileData:
                session["profile_img_url"] = profileData["profile_image_url"]
            else:
                session.pop("profile_img_url", None)
            
            #return redirect(url_for("home"))
            return render_template("public/home.html")
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
            session.pop("profile_img_url", None)
            
            return redirect(url_for("home"))
        else:
            flash("The email address you have entered is already registered")
            return redirect(url_for("signup"))

@app.route("/firebase_logout")
def firebaseLogout():
    logout()
    session.pop("profile_img_url", None)
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
        
        collection.update_one({"_id": getUID()},
                              {"$set":form1},
                              upsert=True
        )
    
    else: 
        print("ERROR")
        
    print("not called")
    
    return render_template("public/home.html")

@app.route("/edit-profile", methods=["POST", "GET"])
def editProfile():
    collection = db["Profile"]
    
    #Imgbb API (upload profile pic to imgbb)
    #f = request.files["editPImage"]
    #f.save(secure_filename(f.filename))
    
    url = "https://api.imgbb.com/1/upload"
    
    image = request.files["editPImage"]
    image_string = base64.b64encode(image.read())
    
    payload = {
        "key": "c92cdfcadffe1289746eca2c06fd5204",
        "image": image_string
    }
    
    res = requests.post(url, payload)  
    imageUrl = res.json()["data"]["image"]["url"]
    
    form = {"_id": getUID(),
            "aboutme": request.form["aboutme"],
            "username": request.form["username"],
            "feet": request.form["feet"],
            "inches": request.form["inches"],
            "weight": request.form["weight"],
            "age": request.form["age"],
            "profile_image_url": imageUrl
                }
    
    collection.update_one({"_id": getUID()},
                          {"$set":form},
                          upsert=True
                          )
    
    session["profile_img_url"] = imageUrl
        
    return redirect(url_for("profile"))