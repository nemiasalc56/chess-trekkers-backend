# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user



# the first users is the blueprint name
# the second argument is its import_name
users = Blueprint('users', 'users')


# register create route
@users.route('/register', methods=['POST'])
def register():

	# get the information from the request
	payload = request.get_json()
	
	# make username lower case
	payload['username'] = payload['username'].lower()
	# check if the username already exists
	try:
		models.User.get(models.User.username == payload['username'])

		# if it does, inform the user
		return jsonify(
			data={},
			message="A user with this username already exists.",
			status=401
			), 200
	# if it doesn't, then create account
	except models.DoesNotExist:

		# create the user with the address
		new_user = models.User.create(
			username= payload['username'],
			password= generate_password_hash(payload['password'])
			)
		# this logs the user and starts a session
		login_user(new_user)

		user_dict = model_to_dict(new_user)
		
		# remove the password
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"Succesfully created user with username {user_dict['username']}",
			status=200
			), 200



# login route
@users.route('/login', methods=['POST'])
def login():
	# get the info from the request
	payload = request.get_json()
	
	# make the username lower case
	payload['username'] = payload['username'].lower()

	try:
		# look use up by username
		user = models.User.get(models.User.username == payload['username']) 
		# this will cause an error if the user doesn't exist

		user_dict = model_to_dict(user)

		# check the password
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		# if the password is good, log user in
		if password_is_good:
			# this logs the user and starts a session
			login_user(user, remember=True)
			# remove the password before we send the information to the user
			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message=f"Succesfully logged in with the username {user_dict['username']}",
				status=200
				), 200
		# if not, inform the user that the username or password is incorrect
		else:
			return jsonify(
				data={},
				message="The username or password is incorrect.",
				status=401
			), 200
	# if we don't find the user
	except models.DoesNotExist:
		# inform user that username or password is incorrect.
		return jsonify(
				data={},
				message="The username or password is incorrect.",
				status=401
		), 201


# user show route
@users.route('/profile', methods=['GET'])
def user_profile():
	
	# look up user with current_user id
	user = models.User.get_by_id(current_user.id)

	# convert to dictionary
	user_dict = model_to_dict(user)
	# remove password
	user_dict.pop('password')
	
	return jsonify(
		data=user_dict,
		message=f"Succesfully found user with id {current_user.id}",
		status=200
		), 200


# logout route
@users.route('/logout', methods=['GET'])
def logout():
	# this is to log user out
	logout_user()
	return jsonify(
		data={},
		message="The user was successfully logged out.",
		status=201
	), 201

# update route
@users.route('/<id>', methods=['PUT'])
def update_user(id):
	# get the info from the body
	payload = request.get_json()
	
	# look up user with the same id
	user = models.User.get_by_id(id)

	# update user info
	user.password = generate_password_hash(payload['password']) if 'password' in payload else None
	user.save()

	# convert model to a dictionary
	user_dict = model_to_dict(user)

	# remove the password
	user_dict.pop('password')

	return jsonify(
		data=user_dict,
		message="Succesfully update the user information",
		status=200
		),200


# destroy route
@users.route('/<id>', methods=['Delete'])
def delete_user(id):

	# look up user
	user = models.User.get_by_id(id)

	# look up user address
	user_address = models.Address.get_by_id(user.address.id)

	# delete address
	user_address.delete_instance(recursive=True)
	# delete user
	user.delete_instance(recursive=True)

	return jsonify(
		data={},
		message="Succesfully deleted user account.",
		status=200
		), 200


# check who is logged in
@users.route('/logged_in', methods=['GET'])
def logged_in():

	if not current_user.is_authenticated:
		return jsonify(
		data={},
		message="No user is currently logged in.",
		status=401
		), 200
	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message="Found logged in user",
			status=200
		), 200