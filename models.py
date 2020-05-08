from peewee import *
import datetime
from flask_login import UserMixin



# using sqlite to have a database
DATABASE = SqliteDatabase('users.sqlite')




# define our model
class User(UserMixin, Model):
	username = CharField(unique=True)
	password = CharField()

	# this gives our class instructions on how to connect to a specific databse
	class Meta:
		database = DATABASE


class Score(Model):
	owner = ForeignKeyField(User, backref='scores')
	high_score = CharField() 
	rank = CharField()
	date = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE





# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Score], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()