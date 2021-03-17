from flask import Flask, render_template
import pymongo
from pymongo import MongoClient

import json
from bson import json_util

cluster = MongoClient(
    "mongodb+srv://new-user_su:147su0@cluster0.tfjyq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

#db = cluster["Health"]
db = cluster.Health
collection = db["Dog"]

app = Flask(__name__)


@app.route("/")
def home():
    # return "welcome"
    return render_template("login.html")


# @app.route("/login", methods=["GET"])
@app.route("/login")
def profile():
    all_seeds = list(collection.find({}))
    # return json.dumps(all_seeds, default=json_util.default)
    return render_template("profile.html", all_seeds=all_seeds)
    #return render_template("profile.html")
    # return "HELLO"


if __name__ == "__main__":
    app.run()
