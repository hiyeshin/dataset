# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

# our demo model from week 5 in class
class Log(Document):
	text = StringField()
	timestamp = DateTimeField(default=datetime.now())

# class Comment(EmbeddedDocument):
# 	name = StringField()
# 	comment = StringField()
# 	timestamp = DateTimeField(default=datetime.now())

class User(Document):

	name = StringField(max_length=120, required=True, verbose_name="What's your name?")
	birthplace = StringField(max_length=120, required=True, verbose_name = "In what country were you born?")
	citizenship = StringField(required = True, verbose_name = "Where do you hold your citizenship?")
	longest_residence = StringField(required=True, verbose_name="What country have you lived in longest?")
	language = StringField(required=True, verbose_name="What languages can you speak?")
	countries_lived = StringField(required=True, verbose_name = "In what countries have you lived?")
	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())


# Create a Validation Form from the Idea model
UserForm = model_form(User)

#name
#demographic data (where were you born)
#contry of citizenship
# what country have you been lived longest?
# what language can you speak?
#

