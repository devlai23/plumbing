from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "soccerdb.calingaiy4id.us-east-2.rds.amazonaws.com"
app.config["MYSQL_USER"] = "hog_kim_lai"
app.config["MYSQL_PASSWORD"] = "7BVjbea4jUrF"
app.config["MYSQL_DB"] = "capstone_2223_mochinut"

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analytics.html")
def analytics():
    return render_template("analytics.html")
    
@app.route("/", methods=['POST'])
def post():
    text = request.form
    cur = mysql.connection.cursor()

    check = "SELECT IF(" + text.get("pnumber") + " in (SELECT Customer_ID from Customer), 1, 0)"
    cur.execute(check)
    rv = str(cur.fetchall())

    if rv[2] == '1':
        return render_template("index.html")
    command = "INSERT INTO Customer VALUES(" + text.get("pnumber") + ", \'" + text.get("fname") + "\', \'" + text.get("lname") + "\', CAST(\'" + text.get("bday") + "\' as DATE), \'" + text.get("email") + "\')"
    cur.execute(command)
    mysql.connection.commit()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
