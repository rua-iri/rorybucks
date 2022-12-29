import flask
from passlib import hash
import flask_mysqldb

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


def logInUser(username):
    pass

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
            # logInUser(username)
            return flask.redirect(flask.url_for("dashboard"))
        else:
            flask.flash('User already exists', 'danger')
            return flask.redirect(flask.url_for('register'))

    return flask.render_template('register.html', form=form)

@app.route("/dashboard")
def dashboard():
    return flask.render_template("dashboard.html")


@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)


