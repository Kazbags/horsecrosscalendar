import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests


from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

scopes = 'https://www.googleapis.com/auth/calendar'
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def _force_https():
    # my local dev is set on debug, but on AWS it's not (obviously)
    # I don't need HTTPS on local, change this to whatever condition you want.
    if not app.debug:
        from flask import _request_ctx_stack
        if _request_ctx_stack is not None:
            reqctx = _request_ctx_stack.top
            reqctx.url_adapter.url_scheme = 'https'

app.before_request(_force_https)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


###----- Calendar Events ----->
@app.route("/", methods=["GET", "POST"])
def index():
    #initiallize event list

    #----- Gannochy YesPlan Events ---->
    #Get json from Yesplan API
    yes = requests.get("https://horsecross.yesplan.be/api/events/location%3AGannochy%20date%3A10-11-2020%20status%3Aconfirmed%20%2B%20status%3Ahold%20%2B%20status%3A%22format%20change%22%20%2B%20status%3Apencilled%20%2B%20status%3Asettled%20%2B%20status%3A%22provisionally%20settled%22%20%20%2B%20status%3A%223rd%20party%20event%22%20%2B%20status%3A%22first%20reserve%22%20%2B%20unavalability?api_key=5C76336690A5BFB115651E1D97CD4262")
    # Get dicionary of events
    data = yes.json()
    gannochy = data['data']
    for booking in gannochy:

        booking['starttime'] = booking['starttime'][11:-9]
        booking['endtime'] = booking['endtime'][11:-9]

    #----- Perth Theatre YesPlan Events ---->
    #Get json from Yesplan API
    yes = requests.get("https://horsecross.yesplan.be/api/events/location%3Apt%20date%3A10-11-2020%20status%3Aconfirmed%20%2B%20status%3Ahold%20%2B%20status%3A%22format%20change%22%20%2B%20status%3Apencilled%20%2B%20status%3Asettled%20%2B%20status%3A%22provisionally%20settled%22%20%20%2B%20status%3A%223rd%20party%20event%22%20%2B%20status%3A%22first%20reserve%22%20%2B%20unavalability?api_key=5C76336690A5BFB115651E1D97CD4262")
    # Get dicionary of events
    data = yes.json()
    pt = data['data']
    for booking in pt:

        booking['starttime'] = booking['starttime'][11:-9]
        booking['endtime'] = booking['endtime'][11:-9]

    #----- Studio YesPlan Events ---->
    #Get json from Yesplan API
    yes = requests.get("https://horsecross.yesplan.be/api/events/location%3Ajoan%20date%3A10-11-2020%20status%3Aconfirmed%20%2B%20status%3Ahold%20%2B%20status%3A%22format%20change%22%20%2B%20status%3Apencilled%20%2B%20status%3Asettled%20%2B%20status%3A%22provisionally%20settled%22%20%20%2B%20status%3A%223rd%20party%20event%22%20%2B%20status%3A%22first%20reserve%22%20%2B%20unavalability?api_key=5C76336690A5BFB115651E1D97CD4262")
    # Get dicionary of events
    data = yes.json()
    jks = data['data']
    for booking in jks:

        booking['starttime'] = booking['starttime'][11:-9]
        booking['endtime'] = booking['endtime'][11:-9]

    #----- Norie Miller YesPlan Events ---->
    #Get json from Yesplan API
    yes = requests.get("https://horsecross.yesplan.be/api/events/location%3Anorie%20date%3A05-11-2020%20status%3Aconfirmed%20%2B%20status%3Ahold%20%2B%20status%3A%22format%20change%22%20%2B%20status%3Apencilled%20%2B%20status%3Asettled%20%2B%20status%3A%22provisionally%20settled%22%20%20%2B%20status%3A%223rd%20party%20event%22%20%2B%20status%3A%22first%20reserve%22%20%2B%20unavalability?api_key=5C76336690A5BFB115651E1D97CD4262")
    # Get dicionary of events
    data = yes.json()
    nm = data['data']
    for booking in nm:

        booking['starttime'] = booking['starttime'][11:-9]
        booking['endtime'] = booking['endtime'][11:-9]

    #----- The Space YesPlan Events ---->
    #Get json from Yesplan API
    yes = requests.get("https://horsecross.yesplan.be/api/events/location%3Aspace%20date%3A10-11-2020%20status%3Aconfirmed%20%2B%20status%3Ahold%20%2B%20status%3A%22format%20change%22%20%2B%20status%3Apencilled%20%2B%20status%3Asettled%20%2B%20status%3A%22provisionally%20settled%22%20%20%2B%20status%3A%223rd%20party%20event%22%20%2B%20status%3A%22first%20reserve%22%20%2B%20unavalability?api_key=5C76336690A5BFB115651E1D97CD4262")
    # Get dicionary of events
    data = yes.json()
    space = data['data']
    for booking in space:

        booking['starttime'] = booking['starttime'][11:-9]
        booking['endtime'] = booking['endtime'][11:-9]

    return render_template("index.html", gannochy = gannochy, pt=pt, jks=jks, nm=nm, space=space)


""" Errors """

###----- Errors ----->
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    flash(f"Error {e.code}, {e.name}")
    return redirect("/")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
