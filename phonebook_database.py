# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:40:33 2019

@author: winkl
"""

import sqlite3
import json
import requests

###---creating a database and cursor---###
conn = sqlite3.connect('phonebook2.db')
c = conn.cursor()

###################
"""People Table"""
###################

###---import random names from json file---###
with open('mock_data_people2.js') as people_phonebook:
 phonebook1 = json.load(people_phonebook)
# print(phonebook1)
 
###---Creating a table within the database with column names---###
def create_table_people():
   c.execute('CREATE TABLE IF NOT EXISTS people_table(first_name TEXT , last_name TEXT, address_line_1 TEXT, address_line_2 TEXT, address_line_3 TEXT, postcode TEXT, country TEXT, telephone_number REAL)')
#create_table_people()

###---Adding data from json file of random people to table in database (for loop to loop through values)---###
def data_entry_people():
   for i in range(len(phonebook1)):
       person_info = phonebook1[i]
       first_name = person_info ['first_name']
       last_name = person_info ['last_name']
       address_line_1 = person_info ['address_line_1']
       address_line_2 = person_info ['address_line_2']
       address_line_3 = person_info ['address_line_3']
       country = person_info ['country']
       postcode = person_info ['postcode']
       telephone_number = person_info ['telephone_number']
#       print(first_name, last_name, address_line_1, address_line_2, address_line_3, postcode, country, telephone_number)
       c.execute('INSERT INTO people_table(first_name, last_name, address_line_1, address_line_2, address_line_3, postcode, country, telephone_number) VALUES (?, ?, ?, ? , ? , ? , ?, ?)', (first_name, last_name, address_line_1, address_line_2, address_line_3, postcode, country, telephone_number))
       conn.commit()
#   c.close()
#   conn.close()
#data_entry_people()

###---Retrieving row from table which has "Simmonds" as the value for the column "last_name"---###
def read_from_people_phonebook1():
    c.execute('SELECT * FROM people_table WHERE last_name ="Simmonds" ')
    for row in c.fetchall():
        print(row)
        
#####################
"""Business Table"""
#####################

###---import random business names from json file---###
with open('mock_data_business2.js') as business_phonebook:
 phonebook2 = json.load(business_phonebook)
# print(phonebook2)
 
###---Creating a table within the database with column names---###
def create_table_business():
   c.execute('CREATE TABLE IF NOT EXISTS business_table(business_name TEXT , address_line_1 TEXT, address_line_2 TEXT, address_line_3 TEXT, postcode TEXT, country TEXT, telephone_number REAL, business_category TEXT)')
#create_table_business()

###---Adding data from json file of random businesses to table in database (for loop to loop through values)---###
def data_entry_business():
   for i in range(len(phonebook2)):
       business_info = phonebook2[i]
       business_name = business_info ['business name']
       address_line_1 = business_info ['address_line_1']
       address_line_2 = business_info ['address_line_2']
       address_line_3 = business_info ['address_line_3']
       country = business_info ['country']
       postcode = business_info ['postcode']
       telephone_number = business_info ['telephone_number']
       business_category = business_info ['business_category']
#       print(business_name, address_line_1, address_line_2, address_line_3, postcode, country, telephone_number, business_category)
       c.execute('INSERT INTO business_table(business_name, address_line_1, address_line_2, address_line_3, postcode, country, telephone_number, business_category) VALUES (?, ?, ?, ? , ? , ? , ?, ?)', (business_name, address_line_1, address_line_2, address_line_3, postcode, country, telephone_number, business_category))
       conn.commit()
#   c.close()
#   conn.close()
#data_entry_business()
   
###---Retrieving row from table which has "Home" as the value for the column "business_category"---###
def read_from_business_phonebook_1():
    c.execute('SELECT * FROM business_table WHERE business_category ="Home" ')
    for row in c.fetchall():
        print(row)

#####################
"""Location Table"""
#####################

def create_table_geopointe():
   c.execute('CREATE TABLE IF NOT EXISTS geopointe_table(postcode REAL, longitude REAL,latitude REAL)')
#create_table_geopointe()

###---looking up postcodes from person table---###
postcode_list = []
endpoint_postcode = "https://api.postcodes.io/postcodes/"
def read_postcode_person_phonebook():
    c.execute('SELECT * FROM people_table ')
    for row in c.fetchall():
        if row[5] not in postcode_list:
            postcode_list.append(row[5])
#        print(postcode_list)
     
#read_postcode_person_phonebook()     

###---looking up postcodes from business table---###
def read_postcode_business_phonebook():
    c.execute('SELECT * FROM business_table ')
    for row in c.fetchall():
        if row[4] not in postcode_list:
            postcode_list.append(row[4])
#        print(postcode_list)
     
#read_postcode_business_phonebook()  
   
###---adding postcodes, longitude and latitute to third table---###
def looping_through_postcodes_geopointe():
    for i in range(len(postcode_list)):
        postcode_response = requests.get(endpoint_postcode + postcode_list[i])
        data_postcode = postcode_response.json()
        if data_postcode['status'] == 200:
            postcode = postcode_list[i]
            longitude = data_postcode['result'] ['longitude']
            latitude = data_postcode['result'] ['latitude']
            c.execute('INSERT INTO geopointe_table(postcode,longitude,latitude) VALUES (?, ?, ?)', (postcode,longitude,latitude)) 
        else:
            pass
        conn.commit()
#looping_through_postcodes_geopointe()

#####################
"""Joining Tables"""
#####################

def join_tables():
    c.execute('SELECT longitude, latitude FROM people_table INNER JOIN geopointe_table ON (people_table.postcode = geopointe_table.postcode) WHERE last_name ="Imorts"')
    for row in c.fetchall():
        print(row)
#join_tables()

################
"""TESTING"""
################

#read_from_people_phonebook1()
#read_from_business_phonebook_1()

#closing cursor
c.close()
conn.close()
