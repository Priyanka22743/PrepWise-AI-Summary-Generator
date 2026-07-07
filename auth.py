from flask import request, redirect
import bcrypt
from database import users_collection

def signup_user():

    username = request.form["username"]
    password = request.form["password"]

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({
        "username": username,
        "password": hashed
    })

    return redirect("/")


def login_user():

    username = request.form["username"]
    password = request.form["password"]

    user = users_collection.find_one({"username": username})

    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return redirect("/dashboard")

    return "Invalid Login"