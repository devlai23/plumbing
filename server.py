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
    #cur = mysql.connection.cursor()


    # cur.execute('''SELECT * FROM Customer''')
    # rv = cur.fetchall()
    # customer = str(rv)
    
    #cur.execute('''INSERT INTO Customer VALUES(9178059232, "Jimmy", "Jones", 2000-01-01, "jimmyjones@gmail.com")''')
    #mysql.connection.commit()

    # cur.close()
    return render_template("index.html")
    
@app.route("/", methods=['POST'])
def post():
    text = request.form
    cur = mysql.connection.cursor()

    check = "SELECT IF(" + text.get("pnumber") + " in (SELECT Customer_ID from Customer), 1, 0)"
    print(check)
    print(text.get("pnumber"))
    print(cur.execute(check))
    if cur.execute(check) == 1:
        return render_template("index.html")
    str = "INSERT INTO Customer VALUES(" + text.get("pnumber") + ", \'" + text.get("fname") + "\', \'" + text.get("lname") + "\', CAST(\'" + text.get("bday") + "\' as DATE), \'" + text.get("email") + "\')"
    cur.execute(str)
    mysql.connection.commit()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
