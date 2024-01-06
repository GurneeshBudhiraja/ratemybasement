import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import date
import helpers

# env variables
load_dotenv()
# address API

api = os.getenv("SECRET_KEY")

# configure application
app = Flask(__name__)

# making db

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.Date, default=date.today())
    address = db.Column(db.String(255))
    rent = db.Column(db.String(10), nullable=True)
    years = db.Column(db.String(10), nullable=True)
    clean = db.Column(db.String(20))
    maintain = db.Column(db.String(20))
    amenities = db.Column(db.String(20))
    neighbourhood = db.Column(db.String(20))
    review = db.Column(db.String(150), nullable=True)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
Session(app)

app.secret_key = os.getenv("SESSION_KEY")  # session key


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# homepage
@app.route("/", methods=["GET"])
def index():
    try:
        if request.method == "GET":
            return render_template("index.html", api=api)
        else:
            print("Error(index): POST")
    except Exception as e:
        print(f"Error is {e}")


# checking the address from the database
@app.route("/submit", methods=["GET", "POST"])
def submit():
    try:
        if request.method == "GET":
            return redirect("/")
        elif request.method == "POST":
            address = (request.form.get("address")).strip().title()
            print(address)
            input_search = (
                Reviews.query.filter_by(address=address)
                .order_by(Reviews.id.desc())
                .all()
            )
            input_search = [review.__dict__ for review in input_search]

            session["address"] = address
            session["input_search"] = input_search
            return render_template(
                "result.html", input_search=input_search, a=session["address"]
            )
        else:
            return redirect("/")
    except Exception as e:
        db.session.rollback()
        return redirect("/")


# form for adding a new review
@app.route("/add", methods=["GET", "POST"])
def add():
    try:
        if request.method == "POST":
            address = session.get("address")
            return render_template("add.html", address=address, api=api)
        else:
            return redirect("/")
    except Exception as e:
        print(f"Error is {e}")
        return redirect("/")


# route triggered after the submit button on the new review form
@app.route("/new_review", methods=["GET", "POST"])
def new_review():
    try:
        if request.method == "POST":
            form_data = {
                "address": request.form.get("address"),
                "rent": request.form.get("rent"),
                "years": request.form.get("years"),
                "clean": request.form.get("clean"),
                "maintain": request.form.get("maintain"),
                "amenities": request.form.get("amenities"),
                "neighbourhood": request.form.get("neighbourhood"),
                "review": request.form.get("review"),
            }
            print(form_data)
            data_checked = helpers.check_data(form_data)
            # print(data_checked)
            if data_checked:
                data_prepared = helpers.prepare_data(form_data)
                print(data_prepared)
                insert_response = insert_data(data_prepared)

                if insert_response:
                    print("200")
                else:
                    # not completed
                    print("501")
                return redirect("/")
            else:
                # not completed
                print("501")
            return redirect("/")
        else:
            return redirect("/")

    except Exception as e:
        print(f"Exception is: {e}")
        return redirect("/")


# for signing up
@app.route("/signup")
def signup():
    return render_template("wip.html")


# for logging
@app.route("/login")
def login():
    return render_template("wip.html")


# for inserting data
def insert_data(data_prepared):
    try:
        print(data_prepared)
        new_review = Reviews(
            address=data_prepared["address"],
            rent=data_prepared["rent"],
            years=data_prepared["years"],
            clean=data_prepared["clean"],
            maintain=data_prepared["maintain"],
            amenities=data_prepared["amenities"],
            neighbourhood=data_prepared["neighbourhood"],
            review=data_prepared["review"],
        )
        # adding to the db
        db.session.add(new_review)
        # Commit the changes to the database
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False


# errorhandlers
@app.errorhandler(404)
def method_not_allowed(error):
    return render_template("404.html")


@app.errorhandler(405)
def method_not_allowed(error):
    return redirect("/")



if __name__ == "__main__":
    command = "gunicorn -w 4 -b 0.0.0.0:5500 -t 60 your_app_module:app"
    app.run(debug=True)
 