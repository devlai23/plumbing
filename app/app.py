from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
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
mail = Mail(app)

app.config["MYSQL_HOST"] = "soccerdb.calingaiy4id.us-east-2.rds.amazonaws.com"
app.config["MYSQL_USER"] = "hog_kim_lai"
app.config["MYSQL_PASSWORD"] = "7BVjbea4jUrF"
app.config["MYSQL_DB"] = "capstone_2223_mochinut"
app.secret_key = env.get("APP_SECRET_KEY")

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mochinutloyalty@gmail.com'
app.config['MAIL_PASSWORD'] = 'smbjiqfaqlbwwzpr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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

@app.route("/email.html")
def email():
    return render_template("email.html") 

@app.route("/email.html", methods=['POST'])
def send():
    msg = Message(
                'Hello',
                sender ='mochinutloyalty@gmail.com',
                recipients = ['danhog23@bergen.org']
               )
    msg.body = request.form.getlist('email')[0]
    #msg.attach('header.gif','image/gif',open(join(mail_blueprint.static_folder, 'header.gif'), 'rb').read(), 'inline', headers=[['Content-ID','<Myimage>'],])
    mail.send(msg)
    return render_template("email.html")

@app.route("/analytics.html")
def analytics():
    return render_template("analytics.html") 

@app.route("/table.html")
def table():
    return render_template("table.html")

@app.route("/table.html")
def transferData():
    cur = mysql.connection.cursor()
    mochidata = []
    query = "SELECT * FROM Customer"
    cur.execute(query)
    for i in cur.fetchall():
        mochidata.append(i)
    cur.close()

    template.render(mochidata = mochidata)
    return render_template("table.html")


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
        path3 = ""
        path4 = ""


        # SEARCH FOR NEW MEMBERS
        cshPath = ""
        for file in os.listdir(ROOT_DIR):
            if (file[0] == "B"):
                cshPath = file
                path3 = cshPath
                break
        book = xlrd.open_workbook(cshPath)
        bookSheet = book.sheet_by_index(0)
        for row in range(2, bookSheet.nrows):
            value = re.sub("\\D+", "", str(bookSheet.cell(row, 11).value))
            if value != "": 
                value = str(int(value))
                query = "Select if("+value+ " in (select Customer_ID from Customer), 1, 0)"
                cur.execute(query)
                rv = str(cur.fetchall())
                if rv[2] == '0':
                    Customer_ID = value
                    Customer_Name = str(bookSheet.cell(row, 0).value)
                    Reg_Date = str(bookSheet.cell(row, 10).value)
                    Customer_Bday = str(bookSheet.cell(row, 13).value)
                    Customer_Email = str(bookSheet.cell(row, 14).value)
                    Bonus = str(bookSheet.cell(row, 1).value)
                    Bonus_Used = str(bookSheet.cell(row, 2).value)
                    Sales_Total = str(bookSheet.cell(row, 3).value)
                    Discount_Total = str(bookSheet.cell(row, 4).value)
                    Discount_Ratio = str(bookSheet.cell(row, 5).value)
                    Rank = str(bookSheet.cell(row, 7).value)
                    Visit_Count = str(bookSheet.cell(row, 8).value)
                    Last_Visit_Date = str(bookSheet.cell(row, 9).value)
                    query = "INSERT INTO Customer VALUES(" + Customer_ID + ", \"" + Customer_Name + "\" , \"" + Reg_Date + "\" , \"" + Customer_Bday + "\" , \"" + Customer_Email + "\" , \"" + Bonus + "\" , \"" + Bonus_Used + "\" , \"" + Sales_Total + "\" , \"" + Discount_Total + "\" , \"" + Discount_Ratio + "\" ," + Rank + " ," + Visit_Count + " , \"" + Last_Visit_Date + "\")"
                    cur.execute(query)
                    mysql.connection.commit()


        # SEARCH FOR NEW ORDERS
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


        # LINK ALL NEW ORDERS TO A CUSTOMER ID
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

        # ADDING NEW ORDERS INTO THE DATABASE
        for order in newOrders:
            if order.customerID != -1:
                cur.execute("select if("+ str(order.customerID) +" in (select Customer_ID from Customer), 1, 0)")
                exists = str(cur.fetchall())
                if exists[2] == "1":
                    cur.execute(order.insertQuery())
                    mysql.connection.commit()

        #Update all existing customer fields (Bonus, Bonus used, Sales total, etc. )
        book = xlrd.open_workbook(path3)
        bookSheet = book.sheet_by_index(0)
        for row in range(6, bookSheet.nrows):
            value = re.sub("\\D+", "", str(bookSheet.cell(row, 11).value))
            name = str(bookSheet.cell(row, 0).value)
            if(name == "Customer" or name == ""):
                continue
            bonus = str(bookSheet.cell(row, 1).value)
            bonusUsed = str(bookSheet.cell(row,2).value)
            salesTotal = str(bookSheet.cell(row, 3).value)
            discountTotal = str(bookSheet.cell(row, 4).value)
            discountRatio = str(bookSheet.cell(row, 5).value)
            if(bookSheet.cell(row, 7).value != ""):
                rank = str(int(bookSheet.cell(row, 7).value))
            else:
                rank = None
            if(bookSheet.cell(row, 8).value != ""):
                visitCount = str(int(bookSheet.cell(row, 8).value))
            else:
                visitCount = None
            lastVisitDate = str(bookSheet.cell(row, 9).value)


            if (value != "" ):
                value = str(int(value))
                query = "Select if("+value+ " in (select Customer_ID from Customer), 1, 0)"
                cur.execute(query)
                rv = str(cur.fetchall())
                if rv[2] == '1':
                    query = "update Customer set Customer_Name = \"" + name + "\", Bonus = \"" + bonus + "\", Bonus_Used = \"" + bonusUsed + "\", Sales_Total = \"" + salesTotal + "\", Discount_Total = \"" + discountTotal + "\", Discount_Ratio = \"" + discountRatio + "\", Customer_Rank = " + rank + ", Visit_Count = " + visitCount + ", Last_Visit_Date = \"" + lastVisitDate + "\" where Customer_ID = " + value
                    cur.execute(query)
                    mysql.connection.commit()
                #update Customer set Customer_Name = "Test_User" where Customer_ID = 9999999999


        




        os.remove(path1)
        os.remove(path2)
        os.remove(path3)

        return render_template("analytics.html")

if __name__ == "__main__":
    app.run(debug=True)