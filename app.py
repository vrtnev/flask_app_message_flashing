from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "vrtnevsecretkey"
app.permanent_session_lifetime = timedelta(days=90)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["usrname"]
        session["user"] = user
        flash(f"You have been successfully logged in, {user}", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            user = session["user"]
            flash(f"You have been already logged in, {user}", "info")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been successfully logged out, {user}", "info")
        session.pop("user", None)
        session.pop("email", None)
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)