#!/usr/bin/python

import MySQLdb #Create a connection to MySQL
import sys #import the system library

import random #to sample a random value

from flask import Flask, render_template, request, json, redirect, url_for
#Flask: A python Framework for creating web applications
#render_template : Library used to render the template files
#json: used to return json data
#request: Library used to read the posted values for the logging and signing up
#redirect: redirects to a url
#url_for: generates an endpoint for the provided method

from flask.ext.mysqldb import MySQL #This library is not working so I used directly MySQLdb instead of Flask-MySQL
#Flask-MySQL library to connect with MySQL for the signing up: We access the table tbl_user into the database bucketlist.
#We also use Flask-MySQL to call the MySQL Stored Procedure, checking that the username doesn't already exist in the database.


from werkzeug import generate_password_hash, check_password_hash
#To create a hashed password

#from jinja2 import Environment, FileSystemLoader
#jinja2 library to print the MySQL requests in the HTML page 'Community'

import os
#To interact with the operating system

from time import time 

from datadog import statsd
# Use Statsd, a Python client for DogStatsd


#tests
statsd.increment('whatever')
statsd.gauge('foo', 42)
statsd.gauge('test1',100)

##Previous connection attempt for the signing up page
##mysql= MySQL()

app = Flask(__name__)


 
@app.route('/')
def main():

	#metric to count the  web.page_view
	statsd.increment('web.page_views',tags = ["page:home"])
	
	#metric to count the overall number of page views
	statsd.increment('web.page_views_total')
	
	"""Render the main page."""
	return render_template('index.html')
	
	
@app.route('/showSignUp')
def showSignUp():


	#metric to count the web.page_views_signup
	statsd.increment('web.page_views_signup',tags = ["page:signup"])
	
	#metric to count the overall number of page views
	statsd.increment('web.page_views_total')
	
	#use of the agent check that samples a random value
	print(random.random())
	
	return render_template('signup.html')
	
	
@app.route('/showCommunity')
def showCommunity():

	#metric to count the web.page_views_community
	statsd.increment('web.page_views_community',tags = ["page:community"])
	
	#metric to count the overall number of page views
	statsd.increment('web.page_views_total')

	#start timer
	start_time = time()
	print start_time
	#connection to the DB
	connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "cacapipi", db = "bucketlist")
	
	#prepare a cursor object using cursor() method
	cursor = connection.cursor()
	
	#execute the SQL query using execute() method
	cursor.execute("select user_name, user_username, user_password from tbl_user ")
	
	#fetch all the rows from the query
	data = cursor.fetchall()
	
	#print the rows
	
	#THIS_DIR = os.path.dirname(os.path.abspath(__file__))
	# Create the jinja2 environment
    # Notice the use of trim_blocks, which greatly helps control whitespace.
	#j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
	#print j2_env.get_template('community.html').render(items=data)
    
	
	#env = Environment(loader=PackageLoader('app', 'template'))
	#template = env.get_template('community.html')
	#print template.render(items=data)
		
	for row in data:	
		print row[0], row[1]
	
	
	cursor.close()
	
	#close the connection
	connection.close()
	
	#return timer
	duration = time() - start_time
	print duration
	statsd.histogram('database.query.time', duration, tags = ["page:community"])
	statsd.gauge('test2',200)
	#exit the program
	sys.exit()
	
	#return "welcome" #render_template('community.html')

@app.route('/showFriends')	
def showFriends():

	#metric to count the web.page_views_friends
	statsd.increment('web.page_views_friends',tags = ["page:friends"])
	
	#metric to count the overall number of page views
	statsd.increment('web.page_views_total')

	#start timer
	start_time = time()
	print start_time
	#connection to the DB
	connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "cacapipi", db = "bucketlist")
	
	#prepare a cursor object using cursor() method
	cursor = connection.cursor()
	
	#execute the SQL query using execute() method
	cursor.execute("select user_name, user_username, user_password from tbl_user_friends ")
	
	#fetch all the rows from the query
	data = cursor.fetchall()
	
	#print the rows
	
	#THIS_DIR = os.path.dirname(os.path.abspath(__file__))
	# Create the jinja2 environment
    # Notice the use of trim_blocks, which greatly helps control whitespace.
	#j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
	#print j2_env.get_template('community.html').render(items=data)
    
	
	#env = Environment(loader=PackageLoader('app', 'template'))
	#template = env.get_template('community.html')
	#print template.render(items=data)
		
	for row in data:	
		print row[0], row[1]
	
	
	cursor.close()
	
	#close the connection
	connection.close()
	
	#return timer
	duration = time() - start_time
	print duration
	statsd.histogram('databaseFriends.query.time', duration, tags = ["page:friends"])
	statsd.gauge('test3',300)
	#exit the program
	sys.exit()
	
	
#signUp page Post request is not working - to improve later
@app.route('/signUp',methods=['POST','GET'])
def signUp():
	try:
		#read the posted values from the UI
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
	
		#validate the received values
		if _name and _email and _password: 
			#We call the MySQL
			
			conn = mysql.connect()
			cursor = conn.cursor() #prepare a cursor object using cursor() method
			_hashed_password = generate_password_hash(_password)
			cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
			
			#If the procedure is executed successfully, we commit the changes and return the success message:
			data = cursor.fetchall() #fetch all of the rows from the query
			
			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		
		else:
			return json.dumps({'html':'<span> Enter the required fields</span>'})
	
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()
		
#login page not used for our application. To improve later.		
@app.route('/login', methods=['GET', 'POST'])
def login():

	#metric to count the web.page_views_login
	statsd.increment('web.page_views_login',tags = ["page:login"])
	
	#metric to count the overall number of page views
	statsd.increment('web.page_views_total')
	
	
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('main'))
	return render_template('login.html', error=error)
	
	
if __name__ == "__main__":
	app.debug = True
	app.run()