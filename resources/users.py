# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict





# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# user create route
@users.route('/register', methods=['POST'])
def user_profile():
	# get the information from the reques
	payload = request.get_json()
	print(payload)

	# make it lower case
	payload['username'] = payload['username'].lower()

	try:
		# check if the username already exist
		models.User.get(models.User.username == payload['username'])

		# if it does, inform the user
		return jsonify(
			data={},
			message="A user with this username already exists.",
			status=401
			), 401

	# if it doesn't, then create account
	except models.DoesNotExist:

		# create the user
		new_user = models.User.create(
			username=payload['username']
			)

		user_dict = model_to_dict(new_user)

		return jsonify(
			data=user_dict,
			message=f"Succesfully created user with username {user_dict['username']}",
			status=200
			), 200


# user login route
@users.route('/login', methods=['POST'])
def get_user():
	# get the information from the reques
	payload = request.get_json()
	print(payload)

	payload['username'] = payload['username'].lower()


	try:
		
		user = models.User.get(models.User.username == payload['username'])
		user_dict = model_to_dict(user)

		return jsonify(
			data=user_dict,
			message="Foud user Succesfully",
			status=200
			), 200

	except:
		return jsonify(
			data={},
			message="There is no user with this username",
			status=401
			), 402



