import flask
import passlib
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



print(secretstuff.SecretStuff.db)

mySql = flask_mysqldb.MySQL(app)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm(flask.request.form)
    users = sqlhelpers.Table("users", "name", "username", "email", "password")

    if flask.request.method=="POST" and form.validate():
        pass

    return flask.render_template("register.html", form=form)


@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)

