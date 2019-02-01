
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 09:37:10 2019

@author: Katharina
"""

from flask import Flask, render_template, request

app = Flask(__name__)


#main file will show the index file (which is an extension of the layout file)
#the layout file connects to the ada function & the contact funciton 
@app.route("/")
def hello():
    return render_template("index.html")

#contact on layout file asks for email address and then connects to confirmation function
@app.route("/contact")
def contact():
    return render_template("contact.html", title='This is the page for the contact form')

#confirmation function then calls the confirmation html 
@app.route("/confirmation", methods=['POST'])
def confirmation():
    formdata = request.form
    email = formdata['email']
    result = 'If email is okay, this sentence here will be displayed on the confirmation page'
    return render_template("confirmation.html", **locals())


#this is just an additional option on the layout file to go to the ada page 
@app.route("/ada")
def ada():
    return render_template("ada.html")


#this will not show, unless you type in a name after the / in the browser 
@app.route("/<name>")
def hello_name(name):
    return render_template("hello.html", name=name.title())


if __name__ == "__main__":
    app.run(debug = True)


