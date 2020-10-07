from flask import Flask, redirect, url_for, render_template, request, session, flash
import dbFuncs

app = Flask(__name__)
app.secret_key = "hello"


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Login page
@app.route("/login/", methods=["POST", "GET"])
def login():
    # Check if already logged in
    if ("username" in session and "email" in session and "password" in session):
        flash("You are already logged in.")
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if dbFuncs.check_if_user_exists(username) is False:
            flash("No account with that username, try again.", "info")
            return render_template("login.html")

        else:
            # Get user from database. currUser is a tuple in the form ("username", "email", "password")
            currUser = dbFuncs.get_user(username)
            # If the input password and the user's passwords match, log them in
            if currUser[2] == password:
                session["username"] = username
                session["password"] = password
                session["email"] = currUser[1]
                flash("You've successfully logged in.", "info")
                return redirect(url_for("user"))
            else:
                flash("Wrong password, try again.")
                return render_template("login.html")


# Profile page
@app.route("/user/", methods=["GET", "POST"])
def user():
    # Only allow access to user page if logged in
    if ("username" in session and "email" in session and "password" in session):

        messages = dbFuncs.get_all_messages_sent_to_user(session["username"])
        messageList = []
        # Each message is a tuple in the form of ("sendingUser", "receivingUser", "messageContent")
        for message in messages:
            messageDict = {
                "sendingUser": message[0],
                "messageContent": message[2]
            }
            messageList.append(messageDict)
        return render_template("user.html", username = session["username"], email = session["email"],messageList=messageList)

    else:
        flash("You are not logged in, please login to access your profile page.")
        return redirect(url_for("login"))


# Logout page
@app.route("/logout/", methods=["GET"])
def logout():
    if "username" in session:
        username = session["username"]
        session.pop("username", None)
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
        if (dbFuncs.check_if_user_exists(username) is True):
            flash("That username is taken, choose another.", "info")
            return redirect(url_for("register"))

        else:
            session["username"] = username
            session["email"] = email
            session["password"] = password
            dbFuncs.create_user(username, email, password)
            flash("You've successfully registered! Please login.")
            return redirect(url_for("login"))


@app.route("/messaging/", methods=["POST", "GET"])
def messaging():
    if request.method == "GET":
        if ("username" in session and "email" in session and "password" in session):
            return render_template("messaging.html")

        else:
            flash("You must log in to send a message to another user.")
            return redirect(url_for("login"))

    elif (request.method == "POST"):
        sendingUser = session["username"]
        receivingUser = request.form["recipient"]
        messageContent = request.form["messageContent"]

        if (dbFuncs.check_if_user_exists(receivingUser) is False):
            flash("No user with that username, message NOT sent.", "info")
            return redirect(url_for("messaging"))

        else:
            dbFuncs.create_message(sendingUser, receivingUser, messageContent)
            flash("Message successfully sent!", "info")
            return redirect(url_for("messaging"))


if __name__ == "__main__":
    dbFuncs.create_tables()
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        dbFuncs.clean_up()
