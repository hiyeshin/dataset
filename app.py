# -*- coding: utf-8 -*-
import os, datetime
import re
import requests
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort, jsonify

# import all of mongoengine
from mongoengine import *

# import data models
import models

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

# hardcoded categories for the checkboxes on the form
# --------- Routes ----------

# this is our main page
@app.route("/", methods=['GET','POST'])
def index():

	# get Idea form from models.py
	user_form = models.UserForm(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and user_form.validate():
	
		# get form data - create new idea
		user = models.User()
		user.name = request.form.get('name','anonymous')
		user.birthplace = request.form.get('birthplace','no title')
		user.citizenship = request.form.get('citizenship','no title')
		user.longest_residence = request.form.get('longest_residence','no title')
		user.language = request.form.get('language','no title')
		user.countries_lived = request.form.get('countries_lived','no title')
		user.save() # save it

		# redirect to the new idea page
		return redirect('/thanks' )

	else:

		#for form management, checkboxes are weird (in wtforms)
		#prepare checklist items for form
		#you'll need to take the form checkboxes submitted
		#and idea_form.categories list needs to be populated.
		if request.method=="POST" and request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				user_form.categories.append_entry(c)

		# render the template
		templateData = {
			'users' : models.User.objects(),
			#'categories' : categories,
			'form' : user_form
		}

		return render_template("main.html", **templateData)



@app.route("/thanks")
def thanks():
	return render_template('thanks.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404





@app.route('/data/demographics')
def data_demographics():

	# query for the ideas - return oldest first, limit 10
	users = models.User.objects().order_by('+timestamp')

	if users:

		# list to hold ideas
		public_users = []

		#prep data for json
		for i in users:
			
			tmpUser = {
				'user_name' : i.name,
				'longest_residence' : i.longest_residence,
				'birthplace' : i.birthplace,
				'language': i.language,
				'countries_lived': i.countries_lived,
				'citizenship': i.citizenship,
				'timestamp' : str( i.timestamp )
			}




	# name = StringField(max_length=120, required=True, verbose_name="What's your name?")
	# birthplace = StringField(max_length=120, required=True, verbose_name = "In what country were you born?")
	# citizenship = StringField(required = True, verbose_name = "Where do you hold your citizenship?")
	# longest_residence = StringField(required=True, verbose_name="What country have you lived in longest?")
	# language = StringField(required=True, verbose_name="What languages can you speak?")
	# countries_lived = StringField(required=True, verbose_name = "In what countries have you lived?")
	# # Timestamp will record the date and time idea was created.
	# timestamp = DateTimeField(default=datetime.now())

			# comments / our embedded documents
			#tmpIdea['comments'] = [] # list - will hold all comment dictionaries
			
			# loop through idea comments
			# for c in i.comments:
			# 	comment_dict = {
			# 		'name' : c.name,
			# 		'comment' : c.comment,
			# 		'timestamp' : str( c.timestamp )
			# 	}

			# 	# append comment_dict to ['comments']
			# 	tmpIdea['comments'].append(comment_dict)

			# # insert idea dictionary into public_ideas list
			public_users.append( tmpUser )

		# prepare dictionary for JSON return
		data = {
			'status' : 'OK',
			'users' : public_users
		}

		# jsonify (imported from Flask above)
		# will convert 'data' dictionary and set mime type to 'application/json'
		return jsonify(data)

	else:
		error = {
			'status' : 'error',
			'msg' : 'unable to retrieve ideas'
		}
		return jsonify(error)


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
# _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
# def slugify(text, delim=u'-'):
# 	"""Generates an ASCII-only slug."""
# 	result = []
# 	for word in _punct_re.split(text.lower()):
# 		result.extend(unidecode(word).split())
# 	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	