import flask
from passlib import hash
import flask_mysqldb
import functools

import secretstuff
import sqlhelpers
import forms

app = flask.Flask(__name__)

app.config['MYSQL_HOST'] = secretstuff.SecretStuff.hst
app.config['MYSQL_USER'] = secretstuff.SecretStuff.usr
app.config['MYSQL_PASSWORD'] = secretstuff.SecretStuff.pw
app.config['MYSQL_DB'] = secretstuff.SecretStuff.db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mySql = flask_mysqldb.MySQL(app)


def isLoggedIn(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if "loggedIn" in flask.session:
            return f(*args, *kwargs)
        else:
            flask.flash("Unauthorized, please log in", "danger")
    return wrap


def logInUser(username):
    users = sqlhelpers.Table("users", "name", "username", "email", "password")
    userData = users.getOne("username", username)
    flask.session["loggedIn"] = True
    flask.session["uName"] = username
    flask.session["name"] = userData.get("name")
    flask.session["email"] = userData.get("email")





@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm(flask.request.form)
    users = sqlhelpers.Table("users", "name", "username", "email", "password")

    print(form.validate())


    #if form is submitted
    if flask.request.method == 'POST' and form.validate():
        #collect form data
        username = form.username.data
        email = form.email.data
        name = form.name.data


        #make sure user does not already exist
        if sqlhelpers.isNewUser(username):
            #add the user to mysql and log them in
            password = hash.sha256_crypt.encrypt(form.password.data)
            users.insert(name, username, email, password)
            logInUser(username)
            return flask.redirect(flask.url_for("dashboard"))
        else:
            flask.flash('User already exists', 'danger')
            return flask.redirect(flask.url_for('register'))

    return flask.render_template('register.html', form=form)



@app.route("/login", methods=["GET", "POST"])
def login():

    if flask.request.method=="POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]

        users = sqlhelpers.Table("users", "name", "username", "email", "password")
        usr = users.getOne("username", username)
        hshPassword = usr.get("password")

        if hshPassword is None:
            flask.flash("User not found", "danger")
            return flask.redirect(flask.url_for("login"))
        else:
            if hshPassword==hash.sha256_crypt.encrypt(password):
                logInUser(username)
                flask.flash("Login Successful", "success")
                return flask.redirect(flask.url_for("dashboard"))
            else:
                flask.flash("Error: Password Invalid", "danger")
                return flask.redirect(flask.url_for("login"))


    return flask.render_template("login.html")



@app.route("/logout")
def logout():
    flask.session.clear()
    flask.flash("Logout Sucessful", "success")
    return flask.redirect(flask.url_for("index"))




@app.route("/dashboard")
@isLoggedIn
def dashboard():
    return flask.render_template("dashboard.html", session=flask.session)




@app.route("/")
def index():
    return flask.render_template("index.html")



if __name__=="__main__":
    app.secret_key = secretstuff.SecretStuff.secretKey
    app.run(debug=True)


