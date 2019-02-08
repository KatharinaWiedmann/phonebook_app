# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 16:03:28 2019

@author: Katharina
"""
from phonebook_database import *
from math import radians, sin, asin, cos, atan, atan2, sqrt

#---------------------------------------------#
#Connect to database
#---------------------------------------------#

def getdb():
    try:
        conn = sqlite3.connect('phonebook2.db')
        c = conn.cursor()
        return c
    except:
        return False

'''
#------------------------------------------------------------------#
#------------------------------------------------------------------#
Business phonebook functions
#------------------------------------------------------------------#
#------------------------------------------------------------------#
'''

#---------------------------------------------#
#Filtering Business Table by Business Category
#---------------------------------------------#


##---creates list of all business categories---###
##SELECT DISTINCT SQLitetutorial possible as well ##

def create_business_category_list():
    try:
        c = getdb()
        c.execute('SELECT distinct (business_category) FROM business_table')
        results = c.fetchall()
        new_results = [i[0] for i in results]
    #    print(new_results)
        return new_results
    except:
        return False
#create_business_category_list()


###---Returns all information where business_category = user_category---###
def extract_business_type_list(user_category):
    c = getdb()
    c.execute('SELECT * from business_table INNER JOIN geopointe_table ON (business_table.postcode = geopointe_table.postcode) WHERE business_category =?', (user_category,))
    business_results = [row for row in c.fetchall()]
#    for row in c.fetchall():
#        business_results.append(row)
    print('Lets see the order of the business results', business_results )
    return business_results


###---Generates list of postcodes for businesses from extract_business_type_list()---###
def extract_business_type_postcode_list(user_category):
    business_category_postcode_list = []
    c = getdb()
#    business_results = extract_business_type_list(user_category)
    c.execute('SELECT * from business_table INNER JOIN geopointe_table ON (business_table.postcode = geopointe_table.postcode) WHERE business_category =?', (user_category,))
    for row in c.fetchall():
        if row[4] not in business_category_postcode_list:
            business_category_postcode_list.append(row[4])
    print('see if we get the postcodes', business_category_postcode_list)
    c.close()
    conn.close()
    return(business_category_postcode_list)


###---Getting latitude and longitude from user's postcode---###
def getting_latlong_from_user():
    count = 0
    while count < 3:
        user_location = input(('What postcode would you like to search? ').strip())
        postcode_response = requests.get(endpoint_postcode + user_location)
        data_postcode = postcode_response.json()
        if data_postcode['status'] == 200:
            longitude = data_postcode['result'] ['longitude']
            latitude = data_postcode['result'] ['latitude']
            latlong = [latitude, longitude]
            return latlong
        else:
            print('Postcode not recognized!')
            count += 1
    return False


#---Getting latitude and longitude from business_category_postcode_list---###
def getting_latlong_from_business_category(user_category):
    c = getdb()
    c.execute('SELECT latitude, longitude from business_table INNER JOIN geopointe_table ON (business_table.postcode = geopointe_table.postcode) WHERE business_category =?', (user_category,))
    results = c.fetchall()
#    print('number of results', results)
    if results == []:
        print('This is an empty list')
        return False
    else:
        return results


###---Calculating distance between user's postcode and postcodes in database---###
def calculate_haversine_distance(latlong, results):
    try:
        distance_list = []
        lat2 = radians(latlong[0])
        lon2 = radians(latlong[1])
        print(lat2,lon2)
        for item in results:
           lat1 = radians((item[0]))
           lon1 = radians((item[1]))
#           print('This is lat1',lat1)
#           print('This is lon1',lon1)
           dlon = lon2 - lon1
#           print('This is dlon: ',dlon)
           dlat = lat2 - lat1
#           print('This is dlat: ',dlat)
           a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
#           print('This is a: ',a)
           c = 2 * atan2( sqrt(a), sqrt(1-a))
#           print('This is c: ',c)
           d = 6371 * c
#           print('This is the distance in km: ',d)
           d_rounded = float("{0:.2f}".format(d))
#           print('This is the rounded distance in km: ',d_rounded)
           distance_list.append(d_rounded)
        return distance_list
    except TypeError:
        print('Please enter a valid postcode')


def create_unsorted_dictionary(distance_list, business_results):
#    distance_postcode_dictionary = dict(zip(distance_list,business_results))
    distance_postcode_dictionary = {}
    count = 0
    for distance in distance_list:
        distance_postcode_dictionary[distance] = business_results[count]
        count += 1
    return distance_postcode_dictionary


def create_distance_postcode_dictionary(distance_postcode_dictionary):
    sorted_dictionary = sorted(distance_postcode_dictionary.items(), key= lambda kv:kv[0])
    print('\nSorted Dictionary:', sorted_dictionary)
    return sorted_dictionary


###---user inputs which business type to filter results by---###
def sort_business_type():
    count = 0
    while count < 3:
        business_category_list = create_business_category_list()
        user_category = input('Choose one of the following business types{}'.format(business_category_list))
        user_category = user_category.title().strip()
        if user_category in business_category_list:
            business_results = extract_business_type_list(user_category)
    #            business_category_postcode_list = extract_business_type_postcode_list(user_category)
            latlong = getting_latlong_from_user()
        # function will only be run if the user inputs a valid postcode
            if latlong!= False:
                print('This is the latlong', latlong)
                results = getting_latlong_from_business_category(user_category)
                distance_list = calculate_haversine_distance(latlong, results)
                print('This is the list of distances', distance_list)

            #create dictionary
                distance_postcode_dictionary = create_unsorted_dictionary(distance_list, business_results)
            #sorted by location
                sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)
#                print(sorted_dictionary)
            #sorted alphabetically
                alphabetically_sorted_dictionary = sort_alphabetically_business(distance_postcode_dictionary)
                if alphabetically_sorted_dictionary != False:
                    print('A to Z dictionary: ', alphabetically_sorted_dictionary)
                    return alphabetically_sorted_dictionary
                else:
                    print("Sorted by Location: ",sorted_dictionary)
                    return sorted_dictionary
        else:
             count += 1
             print('Please only type in a category from the list')
    else:
        print('You have entered an invalid input too many times.')


#---------------------------------------------#
#Filtering Business Table by Business Name
#---------------------------------------------#

def extract_business_name_list(user_name):
    c = getdb()
    c.execute('SELECT * from business_table INNER JOIN geopointe_table ON (business_table.postcode = geopointe_table.postcode) WHERE business_name like ?', ("%"+user_name+"%",))
    business_name_results = [row for row in c.fetchall()]
    if business_name_results == []:
        print('Business name not in phonebook. Please try again.')
        return False
    else:
#        print('Lets see the order of the business results', business_name_results )
        return business_name_results


def getting_latlong_from_business_name(user_name):
    c = getdb()
    c.execute('SELECT latitude, longitude from business_table INNER JOIN geopointe_table ON (business_table.postcode = geopointe_table.postcode) WHERE business_name like ?', ("%"+user_name+"%",))
    results = c.fetchall()
    print('number of results', results)
    if results == []:
        print('This is an empty list')
        return False
    else:
        return results


def create_business_name_list():
    try:
        c = getdb()
        c.execute('SELECT distinct (business_name) FROM business_table')
        results = c.fetchall()
        new_results = [i[0] for i in results]
    #    print(new_results)
        return new_results
    except:
        return False


def sort_alphabetically_business(distance_postcode_dictionary):
    count = 0
    while count < 3:
        sort_a_to_z = input("Would you like to sort the results alphabetically instead? ")
        sort_a_to_z = sort_a_to_z.lower()[0]
        if sort_a_to_z =="y":
            print('sort alphabetically')
            alphabetically_sorted_dictionary = sorted(distance_postcode_dictionary.items(), key= lambda kv:kv[1][0])
            return alphabetically_sorted_dictionary
        elif sort_a_to_z == "n":
            return False
        else:
            print('Only choose yes or no')
            count +=1
    return False


def sort_business_name():
    count = 0
    while count < 3:
        business_name_list = create_business_name_list()
        user_name = input('What is the name of the business you would like to find? ')
        user_name = user_name.title()
        business_results = extract_business_name_list(user_name)
        # function will only run if the user input is part of the name of at least one business in the phonebook
        if business_results != False:
            latlong = getting_latlong_from_user()
        # function will only be run if the user inputs a valid postcode
            if latlong!= False:
                print('This is the latlong', latlong)
                results = getting_latlong_from_business_name(user_name)
                distance_list = calculate_haversine_distance(latlong, results)
                print('This is the list of distances', distance_list)
            #create dictionary
                distance_postcode_dictionary = create_unsorted_dictionary(distance_list, business_results)
            #sorted by location
                sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)
#                print(sorted_dictionary)
            #sorted alphabetically
                alphabetically_sorted_dictionary = sort_alphabetically_business(distance_postcode_dictionary)
                if alphabetically_sorted_dictionary != False:
                    print('A to Z dictionary: ', alphabetically_sorted_dictionary)
                    return alphabetically_sorted_dictionary
                else:
                    print("Sorted by Location: ",sorted_dictionary)
                    return sorted_dictionary
        else:
            count += 1
    print('You have entered an invalid input too many times.')


#------------------------------------------------------------------#
#Function for choosing to search by business type or business name
#------------------------------------------------------------------#

def choose_search_type_business():
    count = 0
    while count < 3:
        try:
            search_type = int(input('''Do you want to search a business by :
                (1) business type
                or
                (2) business name
                or
                (3) Return to main page ? '''))
            if search_type == 1:
                sort_business_type()
            elif search_type == 2:
                sort_business_name()
            elif search_type == 3:
                break
            else:
                count += 1
                if count < 3:
                    print('Please only choose 1, 2 or 3 ')
        except ValueError:
            count += 1
            if count < 3:
                print('Please only choose 1, 2 or 3 ')
    print('Returning to main page')
    return count


'''
#------------------------------------------------------------------#
#------------------------------------------------------------------#
People phonebook functions
#------------------------------------------------------------------#
#------------------------------------------------------------------#
'''
#---------------------------------------------#
#Filtering People Table by Persons Surname
#---------------------------------------------#

def extract_people_name_list(user_name):
    c = getdb()
    c.execute('SELECT * from people_table INNER JOIN geopointe_table ON (people_table.postcode = geopointe_table.postcode) WHERE last_name like ?', ("%"+user_name+"%",))
    people_name_results = [row for row in c.fetchall()]
    #c.close()
    #conn.close()
    if people_name_results == []:
        print('Person\'s name not in phonebook. Please try again.')
        return False
    else:
        print('Lets see the order of the people results', people_name_results )
        return people_name_results


def getting_latlong_from_people_name(user_name):
    c = getdb()
    c.execute('SELECT latitude, longitude from people_table INNER JOIN geopointe_table ON (people_table.postcode = geopointe_table.postcode) WHERE last_name like ?', ("%"+user_name+"%",))
    results = c.fetchall()
    #c.close()
    #conn.close()
    print('number of results', results)
    if results == []:
        print('This is an empty list')
        return False
    else:
        return results


def create_people_name_list():
    try:
        c = getdb()
        c.execute('SELECT distinct (people_name) FROM people_table')
        results = c.fetchall()
        new_results = [i[0] for i in results]
    #    print(new_results)
        #c.close()
        #conn.close()
        return new_results
    except:
        return False


def sort_alphabetically_people(distance_postcode_dictionary):
    count = 0
    while count < 3:
        sort_a_to_z = input("Would you like to sort the results alphabetically instead? ")
        sort_a_to_z = sort_a_to_z.lower()[0]
        if sort_a_to_z =="y":
            print('sort alphabetically')
            alphabetically_sorted_dictionary = sorted(distance_postcode_dictionary.items(), key= lambda kv:kv[1][1])
            return alphabetically_sorted_dictionary
        elif sort_a_to_z == "n":
            return False
        else:
            print('Only choose yes or no')
            count +=1
    return False


def sort_people_surname():
    count = 0
    while count < 3:
        people_name_list = create_people_name_list()
        user_name = input('What is the surname of the person you would like to find? ')
        user_name = user_name.title()
        people_results = extract_people_name_list(user_name)
        # function will only run if the user input is part of the name of at least one business in the phonebook
        if people_results != False:
            latlong = getting_latlong_from_user()
        # function will only be run if the user inputs a valid postcode
            if latlong!= False:
                print('This is the latlong', latlong)
                results = getting_latlong_from_people_name(user_name)
                distance_list = calculate_haversine_distance(latlong, results)
                print('This is the list of distances', distance_list)
            #create dictionary
                distance_postcode_dictionary = create_unsorted_dictionary(distance_list, people_results)
            #sorted by location
                sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)
#                print(sorted_dictionary)
            #sorted alphabetically
                alphabetically_sorted_dictionary = sort_alphabetically_people(distance_postcode_dictionary)
                if alphabetically_sorted_dictionary != False:
                    print('A to Z dictionary: ', alphabetically_sorted_dictionary)
                    return alphabetically_sorted_dictionary
                else:
                    print("Sorted by Location: ",sorted_dictionary)
                    return sorted_dictionary
        else:
            count += 1
    print('You have entered an invalid input too many times.')



#------------------------------------------------------------------#
#Function for choosing to search by surname or returning to main page
#------------------------------------------------------------------#

def choose_search_type_person():
    count = 0
    while count < 3:
        try:
            search_type = int(input('''Do you want to:
                (1) search for a person
                or
                (2) Return to main page ? '''))
            if search_type == 1:
                sort_people_surname()
            elif search_type == 2:
                break
            else:
                count += 1
                if count < 3:
                    print('Please only choose 1 or 2 ')
        except ValueError:
            count += 1
            if count < 3:
                print('Please only choose 1 or 2 ')
    print('Returning to main page')
    return count



'''
#------------------------------------------------------------------#
#------------------------------------------------------------------#
Function for choosing between business and people phonebook
#------------------------------------------------------------------#
#------------------------------------------------------------------#
'''

def choose_phonebook():
    count = 0
    while count < 3:
        try:
            search_type = int(input('''Do you want to:
                (1) search for a person
                or
                (2) search for a business
                or
                (3) Exit ? '''))
            if search_type == 1:
                choose_search_type_person()
            elif search_type == 2:
                choose_search_type_business()
            elif search_type == 3:
                break
            else:
              count += 1
              if count < 3:
                print('Please only choose 1, 2 or 3 ')

        except ValueError:
            count += 1
            if count < 3:
                print('Please only choose 1, 2 or 3 ')
    print('Exit')
    return count


#---------------------------------------------#
#Testing
#---------------------------------------------#

#sort_business_type()
#sort_business_name()
#sort_people_surname()
#choose_search_type()
#choose_phonebook()
#choose_search_type_person()

"""
#------------------------------------------------#
extra functions for Flask
#-------------------------------------------------#
"""

###---Returns all information for businesses---###
def extract_business_type_table():
    c = getdb()
    c.execute('SELECT * from business_table INNER JOIN geopointe_table ON (business_table.postcode = geopointe_table.postcode)')
    business_table = [row for row in c.fetchall()]
    return business_table

###---Returns all information for businesses---###
def extract_all_people_table():
    c = getdb()
    c.execute('SELECT * from people_table INNER JOIN geopointe_table ON (people_table.postcode = geopointe_table.postcode)')
    people_table = [row for row in c.fetchall()]
    return people_table


###---Getting latitude and longitude from user's postcode using FLask---###
def flask_getting_latlong_from_user(user_location):
    postcode_response = requests.get(endpoint_postcode + user_location)
    data_postcode = postcode_response.json()
    if data_postcode['status'] == 200:
        longitude = data_postcode['result'] ['longitude']
        latitude = data_postcode['result'] ['latitude']
        latlong = [latitude, longitude]
        return latlong
    else:
        print('Postcode not recognized!')

###---Flask: sorting alphabetically---###

def sort_alphabetically_people(distance_postcode_dictionary):
        alphabetically_sorted_dictionary = sorted(distance_postcode_dictionary.items(), key= lambda kv:kv[1][1])
        return alphabetically_sorted_dictionary




###---Flask: search by business type and location---####
def flask_sort_business_category(user_category, user_location):
        business_results = extract_business_type_list(user_category)
        user_LatLong = flask_getting_latlong_from_user(user_location)
        results = getting_latlong_from_business_category(user_category)
        distance_list = calculate_haversine_distance(user_LatLong, results)
        distance_postcode_dictionary = create_unsorted_dictionary(distance_list, business_results)
        sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)
        return sorted_dictionary

###---Flask: search by business name and location---####
def flask_sort_business_name(user_location, user_name, business_results):
    user_LatLong = flask_getting_latlong_from_user(user_location)
    results = getting_latlong_from_business_name(user_name)
    distance_list = calculate_haversine_distance(user_LatLong, results)
    distance_postcode_dictionary = create_unsorted_dictionary(distance_list, business_results)
#    sorted_dictionary = create_distance_postcode_dictionary(distance_postcode_dictionary)
    return distance_postcode_dictionary


###---Flask: search by surname and location---####
def flask_sort_people_surname(user_name, user_location, people_results):
    #user_name = user_name.title()
    user_LatLong = flask_getting_latlong_from_user(user_location)
    if user_LatLong != False:
        results = getting_latlong_from_people_name(user_name)
        distance_list = calculate_haversine_distance(user_LatLong, results)
        distance_postcode_dictionary = create_unsorted_dictionary(distance_list, people_results)
        sorted_dictionary_people = create_distance_postcode_dictionary(distance_postcode_dictionary)
        return sorted_dictionary_people
