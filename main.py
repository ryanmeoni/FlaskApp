from flask import Flask, redirect, url_for, render_template, request, session, flash
import sqlalchemy

app = Flask(__name__)
app.secret_key = "hello"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        session["password"] = password
        return redirect(url_for("user"))


@app.route("/user/")
def user():
    if ("username" in session):
        return render_template("user.html", username = session["username"], email = session["email"])

    else:
        flash("You are not logged in, please login to access user page.")
        return redirect(url_for("login"))


@app.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        flash(f"You have logged out, {user}", "info")
        return redirect(url_for("login"))

    else:
        flash("You are not logged in.", "info")
        return redirect(url_for("login"))

@app.route("/register/")
def register():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        user = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        session["user"] = user
        session["email"] = email
        session["password"] = password
        return redirect(url_for("user"))

if __name__ == "__main__":
    app.run(debug=True)
