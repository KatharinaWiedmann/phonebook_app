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
def searchbusiness():
    business_types = create_business_category_list()
    if request.method == 'GET':
        return render_template("searchbusiness.html", title="Business Search", business_types=business_types)

    elif request.method == 'POST':
        form_data = request.form
        user_location = form_data["location"]
        user_category = form_data["business_type"]
        user_name = form_data["business_name"]

        if user_category!="None" and user_name=="" and user_location:
            sorted_dictionary = flask_sort_business_category(user_category, user_location)

        elif user_category=="None" and user_name and user_location:
            business_name_list = create_business_name_list()
            business_results = extract_business_name_list(user_name)
            if business_results != False:
                user_LatLong = flask_getting_latlong_from_user(user_location)
                results = getting_latlong_from_business_name(user_name)
                distance_list = calculate_haversine_distance(user_LatLong, results)
                distance_postcode_dictionary = create_unsorted_dictionary(distance_list, business_results)
                sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)

        else:
            seaching_both = True

        return render_template("searchbusiness.html", title="Business Search", **locals())

@app.route("/searchpeople", methods=['GET', 'POST'])
def searchpeople():
    if request.method == 'GET':
        return render_template("searchpeople.html", title="People Search")

    elif request.method == 'POST':
        form_data = request.form
        user_location = form_data["location"]
        user_name = form_data["last_name"]
        #user_name = user_name.title()
        people_name_list = create_people_name_list()
        people_results = extract_people_name_list(user_name)
        if people_results != False:
            user_LatLong = flask_getting_latlong_from_user(user_location)
            if user_LatLong != False:
                results = getting_latlong_from_people_name(user_name)
                distance_list = calculate_haversine_distance(user_LatLong, results)
                distance_postcode_dictionary = create_unsorted_dictionary(distance_list, people_results)
                sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)



        #sorted_dictionary = flask_sort_people_surname(user_name, user_location)


    return render_template("searchpeople.html", title="People Search", **locals())

if __name__ == "__main__":
    app.run(debug = True)
