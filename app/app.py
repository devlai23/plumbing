from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
import os
import xlrd
import re
import base64
from jinja2 import Environment, FileSystemLoader
import datetime
from functools import wraps

ROOT_DIR = os.path.abspath(os.curdir)
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
mail = Mail(app)

app.config["MYSQL_HOST"] = "soccerdb.calingaiy4id.us-east-2.rds.amazonaws.com"
app.config["MYSQL_USER"] = "hog_kim_lai"
app.config["MYSQL_PASSWORD"] = "7BVjbea4jUrF"
app.config["MYSQL_DB"] = "capstone_2223_mochinut"
app.secret_key = env.get("APP_SECRET_KEY")

# configuration of mail
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'mochinutloyalty@gmail.com'
# app.config['MAIL_PASSWORD'] = 'smbjiqfaqlbwwzpr' 
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SERVER']='secure.emailsrvr.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@mochinut-tenafly.com'
app.config['MAIL_PASSWORD'] = 'Work4God1' 
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

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        access_token = session['user']['access_token']
        if not access_token:
            return redirect('/')
        try:
            return f(*args, **kwargs)
        except:
            return redirect('/')
    return decorated

@app.route("/")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/index.html")
@requires_auth
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
@requires_auth
def email():
    return render_template("email.html") 

@app.route("/send-manually", methods=['GET', 'POST'])
def send():
    send_type = request.form.get('send-option')
    print("send_type:", send_type)

    # if code can be streamlined
    if send_type == 'send-manually':
        email = request.form['manual_emails']
        emailArr = email.split()
        image = request.files['file']
        text = request.form['textbox']

        image_folder = os.path.join(APP_ROOT, 'images')
        image_path = os.path.join(image_folder, image.filename)
        image.save(image_path)

        with open(image_path, 'rb') as f:
            image_data = f.read()

        encoded_image = base64.b64encode(image_data).decode('utf-8')
        msg = Message('Image', sender="info@mochinut-tenafly.com", recipients=emailArr)
        with open(os.path.join(APP_ROOT, 'email_template.html'), 'r') as f:
            email_template = f.read()

        # attach the image to the email
        with app.open_resource(image_path) as fp:
            msg.attach(image.filename, 'image/png', fp.read(), 'inline', headers=[['Content-ID','<image>']])

        # set the HTML content with a reference to the attached image
        msg.html = email_template.format(image_cid='image', text=text)
        mail.send(msg)

        email_sent = True

        print("email_sent:", email_sent)


        return render_template('email.html', email_sent=email_sent)
    
    elif send_type == 'send-all':
        #RUN QUERY TO GET ARRAY WITH ALL EMAIL ADDRESSES
        emailArr = QUERY

        image = request.files['file']
        text = request.form['textbox']

        image_folder = os.path.join(APP_ROOT, 'images')
        image_path = os.path.join(image_folder, image.filename)
        image.save(image_path)

        with open(image_path, 'rb') as f:
            image_data = f.read()

        encoded_image = base64.b64encode(image_data).decode('utf-8')
        msg = Message('Image', sender="info@mochinut-tenafly.com", recipients=emailArr)
        with open(os.path.join(APP_ROOT, 'email_template.html'), 'r') as f:
            email_template = f.read()

        # attach the image to the email
        with app.open_resource(image_path) as fp:
            msg.attach(image.filename, 'image/png', fp.read(), 'inline', headers=[['Content-ID','<image>']])

        # set the HTML content with a reference to the attached image
        msg.html = email_template.format(image_cid='image', text=text)
        mail.send(msg)
        email_sent = True

        return render_template('email.html', email_sent=email_sent)

    elif send_type == 'send-bdays':
        cur = mysql.connection.cursor()
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        # EDIT STARTING HERE
        query = f"SELECT Customer_Email FROM Customer WHERE DATE_FORMAT(Customer_Bday, '%m-%d') BETWEEN '{start_of_week.strftime('%m-%d')}' AND '{end_of_week.strftime('%m-%d')}'"
        cur.execute(query)
        rv = str(cur.fetchall())

        print(rv); 

        bday_emails = []
        
        
        # image = request.files['file']
        # text = request.form['textbox']

        # image_folder = os.path.join(APP_ROOT, 'images')
        # image_path = os.path.join(image_folder, image.filename)
        # image.save(image_path)

        # with open(image_path, 'rb') as f:
        #     image_data = f.read()

        # encoded_image = base64.b64encode(image_data).decode('utf-8')
        # msg = Message('Image', sender="mochinutloyalty@gmail.com", recipients=emailArr)
        # with open(os.path.join(APP_ROOT, 'email_template.html'), 'r') as f:
        #     email_template = f.read()

        # # attach the image to the email
        # with app.open_resource(image_path) as fp:
        #     msg.attach(image.filename, 'image/png', fp.read(), 'inline', headers=[['Content-ID','<image>']])

        # # set the HTML content with a reference to the attached image
        # msg.html = email_template.format(image_cid='image', text=text)
        # mail.send(msg)
        email_sent = True


        return render_template('email.html', email_sent=email_sent)

    else:
        email_sent = False

        print("email_sent:", email_sent)

        return render_template('email.html', email_sent=email_sent)
    

@app.route("/analytics.html")
@requires_auth
def analytics():
    #if 'mybutton' in request.form:
    cur = mysql.connection.cursor()
    query = "SELECT item, COUNT(*) AS popularity FROM Purchases GROUP BY item ORDER BY popularity DESC LIMIT 5"
    cur.execute(query)
    rows = cur.fetchall()
    popular_items = []
    for row in rows:
        popular_items.append((row[0], row[1]))
    #return render_template('analytics.html', chart_data=popular_items) 
    #elif 'buyerButton' in request.form:
    top_buyers = []
    top_buyers = request.args.get('top-buyers')
    top_buyersMilkTea = []
    selected = request.args.get('selected')
    cur = mysql.connection.cursor()
    queryMochi = f"select Purchases.Item, Customer.Customer_Name, count(*) from Purchases INNER JOIN Customer ON Purchases.Customer_ID=Customer.Customer_ID where Purchases.Item like \"1 MOCHINUT\" Group By Customer.Customer_Name Order by count(*) DESC LIMIT 5;"
    cur.execute(queryMochi)
    queryBubbleTea = f"select Purchases.Item, Customer.Customer_Name, count(*) from Purchases INNER JOIN Customer ON Purchases.Customer_ID=Customer.Customer_ID where Purchases.Item like \"MILKTEA\" Group By Customer.Customer_Name Order by count(*) DESC LIMIT 5;"
    topBuyerRows = cur.fetchall()
    cur.execute(queryBubbleTea)
    topBubbleRows = cur.fetchall()
    if topBuyerRows:
        top_buyers = [row[1] for row in topBuyerRows]
    else:
        top_buyers = []
    if topBubbleRows:
        top_buyersMilkTea = [row[1] for row in topBubbleRows]
    else:
        top_buyersMilkTea = []
    #return render_template('analytics.html', topBuyers=top_buyers, selected = selected, top_buyersMilkTea= top_buyersMilkTea)
    return render_template('analytics.html', chart_data=popular_items, topBuyers=top_buyers, selected = selected, top_buyersMilkTea= top_buyersMilkTea)  

    
@app.route("/table.html")
@requires_auth
def table():
    # environment = Environment(loader=FileSystemLoader("app/templates/"))
    #template = environment.get_template("table.html")
    cur = mysql.connection.cursor()
    mochidata = []
    query = "SELECT * FROM Customer"
    cur.execute(query)
    for data in cur.fetchall():
        mochidata.append(data)
    cur.close()

    return render_template("table.html", mochidata=mochidata)

@app.route('/latest.html')
@requires_auth
def new_page():
    cur = mysql.connection.cursor()
    query = """SELECT *
            FROM Customer
            WHERE STR_TO_DATE(Reg_Date, '%m/%d/%y %h:%i:%s %p') BETWEEN DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 MONTH), '%Y-%m-01') AND LAST_DAY(DATE_SUB(NOW(), INTERVAL 1 MONTH))
            UNION
            SELECT *
            FROM Customer
            WHERE STR_TO_DATE(Reg_Date, '%m/%d/%y %h:%i:%s %p') BETWEEN DATE_FORMAT(NOW(), '%Y-%m-01') AND LAST_DAY(NOW());"""
    cur.execute(query)
    rv = str(cur.fetchall())
    data = eval(rv)
    message = ""
    for inner_tuple in data:
        message += str(inner_tuple[:5])
    return render_template('latest.html', message=message)

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
        return "Phone number already exists"
    now = datetime.datetime.now()
    formatted_date = now.strftime('%m/%d/%y %#I:%M:%S %p')
    command = "INSERT INTO Customer (Customer_ID, Customer_Name, Customer_Bday, Customer_Email, Reg_Date) VALUES (" + "\"" + text.get("pnumber") + "\"" + ", " + "\"" + text.get("lname") + ", " + text.get("fname") + "\", "  + "\"" + text.get("bday") + "\"" + ", " + "\"" + text.get("email") + "\", " + "\"" + formatted_date + "\"" + ")"
    cur.execute(command)
    mysql.connection.commit()
    cur.close()
    return render_template("index.html")

@app.route("/success", methods = ['POST'])
def success():  
    # needs bonus mileage, customer history, customer sales history
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

        # SEARCH FOR NEW MEMBERS
        cshPath = ""
        for file in os.listdir(ROOT_DIR):
            if (file[0] == "B"):
                cshPath = file
                path3 = cshPath
                break
        book = xlrd.open_workbook(cshPath)
        bookSheet = book.sheet_by_index(0)
        count = 0
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
                    count+=1
        print("TESTFLOW:", str(count), "new members were successfully added to the database")


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
        print("TESTFLOW:", str(len(newOrders)), "new orders were found")

        # LINK ALL NEW ORDERS TO A CUSTOMER ID
        cshPath = ""
        count = 0
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
                        count += 1
        print("TESTFLOW:", count, "CustomerID's were linked to new orders")

        # ADDING NEW ORDERS INTO THE DATABASE
        count = 0
        for order in newOrders:
            if order.customerID != -1:
                cur.execute("select if("+ str(order.customerID) +" in (select Customer_ID from Customer), 1, 0)")
                exists = str(cur.fetchall())
                if exists[2] == "1":
                    cur.execute(order.insertQuery())
                    mysql.connection.commit()
                    count +=1
        print("TESTFLOW:", count, "orders were successfully added to the database")

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
        print("Other fields for all customers have been updated")

        os.remove(path1)
        os.remove(path2)
        os.remove(path3)
        cur.close()
        return render_template("analytics.html")

class Order:
    def __init__(self, invoiceID, date, item):
        self.invoiceID = invoiceID
        self.date = date
        self.item = item
        self.customerID = -1

    def setCustomerID(self, customerID):
        self.customerID = customerID

    def getInvoice(self):
        return self.invoiceID

    def getDate(self):
        return self.date
    
    def __str__(self):
     return str(self.invoiceID) + "\n" + str(self.date) + "\n" + str(self.item) + "\n" + str(self.customerID) + "\n"

    def insertQuery(self):
        formatted = "INSERT INTO Purchases(Invoice_ID, Item, Customer_ID, Date) VALUES (" + str(self.invoiceID) + ", \"" + str(self.item) + "\", " + str(self.customerID) + ", \"" + str(self.date) + "\")"
        return formatted



if __name__ == "__main__":
    app.run(debug=True)