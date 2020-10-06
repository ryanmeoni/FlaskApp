from flask import Flask, redirect, url_for, render_template, request, session, flash
import dbUserFuncs

app = Flask(__name__)
app.secret_key = "hello"


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Login page
@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if dbUserFuncs.check_if_user_exists(username) is False:
            flash("No account with that username, try again.", "info")
            return render_template("login.html")

        else:
            currUser = dbUserFuncs.get_user(username)
            if currUser[2] == password:
                session["username"] = username
                session["password"] = password
                flash("You've successfully logged in.")
                return redirect(url_for("home"))
            else:
                flash("Wrong password, try again.")
                return render_template("login.html")


# Profile page
@app.route("/user/", methods=["GET", "POST"])
def user():
    if ("username" in session and "email" in session):
        return render_template("user.html", username = session["username"], email = session["email"])

    else:
        flash("You are not logged in, please login to access user page.")
        return redirect(url_for("login"))


# Logout page
@app.route("/logout/", methods=["GET"])
def logout():
    if "username" in session:
        username = session["username"]
        session.pop("user", None)
        flash(f"You have logged out, {username}", "info")
        return redirect(url_for("login"))

    else:
        flash("You are not logged in.", "info")
        return redirect(url_for("login"))


# Register page
@app.route("/register/", methods=["POST", "GET"])
def register():
    print(request.method)
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if username already exists. If so, flash error.
        if (dbUserFuncs.check_if_user_exists(username) is True):
            flash("That username is taken, choose another.", "info")
            return render_template("register.html")

        else:
            session["username"] = username
            session["email"] = email
            session["password"] = password
            dbUserFuncs.create_user(username, email, password)

            flash("You've successfully registered! Please login.")
            return redirect(url_for("login"))


if __name__ == "__main__":
    dbUserFuncs.create_tables()
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        dbUserFuncs.clean_up()
