# -*- coding: utf-8 -*-
import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
from mongoengine import *

# import data models
import models

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
# connect('mydata', host=os.environ.get('MONGOLAB_URI'))
# app.logger.debug("Connecting to MongoLabs")

# hardcoded categories for the checkboxes on the form
#categories = ['web','physical computing','software','video','music','installation','assistive technology','developing nations','business','social networks']

# --------- Routes ----------

# this is our main page
@app.route("/", methods=['GET','POST'])
def index():

	# get Idea form from models.py
	idea_form = models.IdeaForm(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and idea_form.validate():
	
		# get form data - create new idea
		idea = models.Idea()
		idea.creator = request.form.get('creator','anonymous')
		idea.title = request.form.get('title','no title')
		idea.slug = slugify(idea.title + " " + idea.creator)
		idea.idea = request.form.get('idea','')
		#idea.categories = request.form.getlist('categories') # getlist will pull multiple items 'categories' into a list
		
		idea.save() # save it

		# redirect to the new idea page
		return redirect('/ideas/%s' % idea.slug)

	else:

		# for form management, checkboxes are weird (in wtforms)
		# prepare checklist items for form
		# you'll need to take the form checkboxes submitted
		# and idea_form.categories list needs to be populated.
		if request.method=="POST" and request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				idea_form.categories.append_entry(c)

		# render the template
		templateData = {
			#'ideas' : models.Idea.objects(),
			#'categories' : categories,
			'form' : idea_form
		}

		return render_template("main.html", **templateData)

# Display all ideas for a specific category
# @app.route("/category/<cat_name>")
# def by_category(cat_name):

# 	# try and get ideas where cat_name is inside the categories list
# 	try:
# 		ideas = models.Idea.objects(categories=cat_name)

# 	# not found, abort w/ 404 page
# 	except:
# 		abort(404)

# 	# prepare data for template
# 	templateData = {
# 		'current_category' : {
# 			'slug' : cat_name,
# 			'name' : cat_name.replace('_',' ')
# 		},
# 		'ideas' : ideas,
# 		'categories' : categories
# 	}

# 	# render and return template
# 	return render_template('category_listing.html', **templateData)


# @app.route("/ideas/<idea_slug>")
# def idea_display(idea_slug):

# 	# get idea by idea_slug
# 	try:
# 		idea = models.Idea.objects.get(slug=idea_slug)
# 	except:
# 		abort(404)

# 	# prepare template data
# 	templateData = {
# 		'idea' : idea
# 	}

# 	# render and return the template
# 	return render_template('idea_entry.html', **templateData)

# @app.route("/ideas/<idea_slug>/edit", methods=['GET','POST'])
# def idea_edit(idea_slug):

	
# 	# try and get the Idea from the database / 404 if not found
# 	try:
# 		idea = models.Idea.objects.get(slug=idea_slug)
		
# 		# get Idea form from models.py
# 		# if http post, populate with user submitted form data
# 		# else, populate the form with the database record
# 		idea_form = models.IdeaForm(request.form, obj=idea)	
# 	except:
# 		abort(404)

# 	# was post received and was the form valid?
# 	if request.method == "POST" and idea_form.validate():
	
# 		# get form data - update a few fields
# 		# note we're skipping the update of slug (incase anyone has previously bookmarked)
# 		idea.creator = request.form.get('creator','anonymous')
# 		idea.title = request.form.get('title','no title')
# 		idea.idea = request.form.get('idea','')
# 		idea.categories = request.form.getlist('categories')

# 		idea.save() # save changes

# 		return redirect('/ideas/%s/edit' % idea.slug)

# 	else:

# 		# for form management, checkboxes are weird (in wtforms)
# 		# prepare checklist items for form
# 		# you'll need to take the form checkboxes submitted
# 		# and idea_form.categories list needs to be populated.
# 		if request.method=="POST" and request.form.getlist('categories'):
# 			for c in request.form.getlist('categories'):
# 				idea_form.categories.append_entry(c)

# 		templateData = {
# 			'categories' : categories,
# 			'form' : idea_form,
# 			'idea' : idea
# 		}

# 		return render_template("idea_edit.html", **templateData)


# @app.route("/ideas/<idea_id>/comment", methods=['POST'])
# def idea_comment(idea_id):

# 	name = request.form.get('name')
# 	comment = request.form.get('comment')

# 	if name == '' or comment == '':
# 		# no name or comment, return to page
# 		return redirect(request.referrer)


# 	#get the idea by id
# 	try:
# 		idea = models.Idea.objects.get(id=idea_id)
# 	except:
# 		# error, return to where you came from
# 		return redirect(request.referrer)


# 	# create comment
# 	comment = models.Comment()
# 	comment.name = request.form.get('name')
# 	comment.comment = request.form.get('comment')
	
# 	# append comment to idea
# 	idea.comments.append(comment)

# 	# save it
# 	idea.save()

# 	return redirect('/ideas/%s' % idea.slug)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	