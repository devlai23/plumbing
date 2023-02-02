from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
import Order
import os
import xlwt
import xlrd
from xlutils.copy import copy
import sys
import re

ROOT_DIR = os.path.abspath(os.curdir)
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

app.config["MYSQL_HOST"] = "soccerdb.calingaiy4id.us-east-2.rds.amazonaws.com"
app.config["MYSQL_USER"] = "hog_kim_lai"
app.config["MYSQL_PASSWORD"] = "7BVjbea4jUrF"
app.config["MYSQL_DB"] = "capstone_2223_mochinut"
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

mysql = MySQL(app)

@app.route("/")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/index.html")

@app.route("/logout.html")
def logout():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("out", _external=True)
    )

@app.route("/out")
def out():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("login", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/analytics.html")
def analytics():
    return render_template("analytics.html") 

@app.route("/", methods=['POST'])
def log():
    return render_template("index.html")
    
@app.route("/index.html", methods=['POST'])
def post():
    text = request.form
    cur = mysql.connection.cursor()

    check = "SELECT IF(" + text.get("pnumber") + " in (SELECT Customer_ID from Customer), 1, 0)"
    cur.execute(check)
    rv = str(cur.fetchall())

    if rv[2] == '1':
        return render_template("index.html")
    command = "INSERT INTO Customer (Customer_ID, Customer_Name, Customer_Bday, Customer_Email) VALUES(" + "\"" + text.get("pnumber") + "\"" + ", " + "\"" + text.get("lname") + ", " + text.get("fname") + "\", "  + "\"" + text.get("bday") + "\"" + ", " + "\"" + text.get("email") +  "\")"
    cur.execute(command)
    mysql.connection.commit()
    return render_template("index.html")

@app.route("/success", methods = ['POST'])
def success():  
    if request.method == 'POST':  
        files = request.files.getlist("file")
        for file in files:
            file.save(file.filename)

        #finding lastPos
        cur = mysql.connection.cursor()
        cur.execute("SELECT Invoice_ID from Purchases order by Invoice_ID desc limit 1")
        mysql.connection.commit()
        lastPos = str(cur.fetchall())
        newString = ""
        for char in lastPos:
            if ord(char) > 47 and ord(char) < 58:
                newString += char
        lastPos = int(newString)

        path1 = ""
        path2 = ""
        #looping through excel files
        cshPath = ""
        for file in os.listdir(ROOT_DIR):
            if (file[0:10] == "Customer S"):
                cshPath = file
                path1 = cshPath
                break
        book = xlrd.open_workbook(cshPath)
        bookSheet = book.sheet_by_index(0)
        newOrders = []
        for row in range(0, bookSheet.nrows):
            value = str(bookSheet.cell(row, 0).value)
            newValue = ""
            for char in value:
                if ord(char) > 47 and ord(char) < 58:
                    newValue += char
                else:
                    break
            #if true, it's a new order
            if newValue != "" and int(newValue) > lastPos:
                order = Order.Order(int(newValue), bookSheet.cell(row, 1).value, bookSheet.cell(row, 2).value)
                newOrders.append(order)


        #looping through second file
        cshPath = ""
        for file in os.listdir(ROOT_DIR):
            if (file[0:10] == "Customer H"):
                cshPath = file
                path2 = file
                break
        book = xlrd.open_workbook(cshPath)
        bookSheet = book.sheet_by_index(0)
        for row in range(0, bookSheet.nrows):
            value = str(bookSheet.cell(row, 2).value)
            if value != "" and value != "Invoice #":
                value = int(float(value))
            for order in newOrders:
                if value == order.getInvoice():
                    customerID = str(bookSheet.cell(row, 1).value)
                    if customerID != "":
                    # then this neworder was by a loyalty member. this order must be entered to database
                        newCustomerID = int(re.sub("\\D+", "", customerID))
                        order.setCustomerID(newCustomerID)

        for order in newOrders:
            if order.customerID != -1:
                print(order.insertQuery())
                cur.execute(order.insertQuery())
                mysql.connection.commit()
        

        # os.remove(path1)
        # os.remove(path2)

        return render_template("analytics.html")

if __name__ == "__main__":
    app.run(debug=True)