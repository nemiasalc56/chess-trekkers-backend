from flask import Flask, g
import models
# import our resources
from resources.users import users
from resources.scores import scores
from flask_cors import CORS
from flask_login import LoginManager



DEBUG = True # print the error
PORT = 8000


app = Flask(__name__)
# set up a secret key
app.secret_key = "kjkjsfijs984u39ffn48fjskldf"


# instantiate LoginManager to a login_manager
login_manager = LoginManager()

# connect the app with login_manager
login_manager.init_app(app)


# user loader will use this callback to load the user object
@login_manager.user_loader
def load_user(user_id):
	try:
		# look up user
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():

	return jsonify(
		data={
		'error': 'FORBIDDEN'
		},
		message="You are not allow to do that, you must be logged in",
		status=403
		), 403



CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(scores, origins=['http://localhost:3000'],supports_credentials=True)


# use the blueprint that will handle the users stuff
app.register_blueprint(users, url_prefix='/api/v1/users/')
app.register_blueprint(scores, url_prefix='/api/v1/scores/')


# use this decorator to cause a function to run before request
@app.before_request
def before_request():
	# store the data as a global variable in g
	g.db = models.DATABASE
	g.db.connect()


# use this decorator to cause a function to run after request
@app.after_request
def after_request(response):
	g.db.close()
	return response




if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)