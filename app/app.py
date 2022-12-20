from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from authlib.integrations.flask_client import OAuth

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

# @app.route("/")
# def home():
#     return render_template("login.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/index.html")

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
    command = "INSERT INTO Customer VALUES(" + text.get("pnumber") + ", \'" + text.get("fname") + "\', \'" + text.get("lname") + "\', CAST(\'" + text.get("bday") + "\' as DATE), \'" + text.get("email") + "\')"
    cur.execute(command)
    mysql.connection.commit()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
