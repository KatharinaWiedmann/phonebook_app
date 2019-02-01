from flask import Flask, render_template, request
from business_phonebook_functions import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title="Homepage")

@app.route("/business")
def business():
    business_table = extract_business_type_table()
    return render_template("business.html", title="Business", business_table=business_table)

@app.route("/people")
def people():
    return render_template("people.html", title="People")

if __name__ == "__main__":
    app.run(debug = True)
