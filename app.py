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
    people_table = extract_all_people_table()
    return render_template("people.html", title="People", people_table=people_table)

@app.route("/searchbusiness", methods=['GET', 'POST'])
def businesssearch():
    business_types = create_business_category_list()
    if request.method == 'GET':
        return render_template("searchbusiness.html", title="Business Search", business_types=business_types)

    elif request.method == 'POST':
        form_data = request.form
        user_location = form_data["location"]
        user_category = form_data["business_type"]
        business_results = extract_business_type_list(user_category)
        user_LatLong = flask_getting_latlong_from_user(user_location)
        rresults = getting_latlong_from_business_category(user_category)
        ddistance_list = calculate_haversine_distance(user_LatLong, rresults)
        ddistance_postcode_dictionary = create_unsorted_dictionary(ddistance_list, business_results)
        ssorted_dictionary = create_distance_postcode_dictionary(ddistance_postcode_dictionary)

        return render_template("searchbusiness.html", title="Business Search", **locals())


if __name__ == "__main__":
    app.run(debug = True)
