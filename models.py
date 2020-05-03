from peewee import *
import datetime



# using sqlite to have a database
DATABASE = SqliteDatabase('users.sqlite')




# define our model
class User(Model):
	username = CharField()
	high_score = CharField() 
	rank = CharField()
	date = DateTimeField(default=datetime.datetime.now)

	# this gives our class instructions on how to connect to a specific databse
	class Meta:
		database = DATABASE





# this method will set up the connection to our database
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)

	print("Connected to database and created tables if they weren't already there.")

	DATABASE.close()