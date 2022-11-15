from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "soccerdb.calingaiy4id.us-east-2.rds.amazonaws.com"
app.config["MYSQL_USER"] = "hog_kim_lai"
app.config["MYSQL_PASSWORD"] = "7BVjbea4jUrF"
app.config["MYSQL_DB"] = "capstone_2223_mochinut"

mysql = MySQL(app)

@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Customer')
    rv = cur.fetchall()
    customer = str(rv)
    #cur.execute('INSERT INTO Customer (Customer_ID, First_Name, Last_Name, Birthday, Email) values (9178059231, "Bobby", "Jones", 2005-01-07, "bobbyjones@gmail.com")')
    #return customer
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
