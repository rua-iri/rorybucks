import flask
import passlib
import flask_mysqldb

import secretstuff

app = flask.Flask(__name__)

app.config["MYSQL_HOST"] = secretstuff.SecretStuff.hst
app.config["MYSQL_USER"] = secretstuff.SecretStuff.usr
app.config["MYSQL_PASSWORD"] = secretstuff.SecretStuff.pw
app.config["MYSQL_DATABASE"] = secretstuff.SecretStuff.db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

print(secretstuff.SecretStuff.db)

mySql = flask_mysqldb.MySQL(app)

@app.route("/")

def index():
    return "Hello World!"


if __name__=="__main__":
    app.run(debug=True)

