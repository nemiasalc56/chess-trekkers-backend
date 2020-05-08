# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict



scores = Blueprint('scores', 'scores')


# score create route
@scores.route('/', methods=['POST'])
def score():
	# get the information from the reques
	payload = request.get_json()
	print(payload)

	# create the score
	new_score = models.Score.create(
		owner=current_user.id,
		high_score=payload['high_score'],
		rank=payload['rank']
		)

	score_dict = model_to_dict(new_score)
	score_dict['owner'].pop('password')
	print(score_dict['owner'])

	return jsonify(
		data=score_dict,
		message="Succesfully created score",
		status=200
		), 200


# score get route
@scores.route('/', methods=['GET'])
def get_score():
	# get the information from the reques
	payload = request.get_json()
	print(payload)

	# create the score
	# user_score = models.Score.get(models.Score.owner == current_user.id)
	user_scores = models.Score.select()

	print("printing user_score")

	score_dict = [model_to_dict(score) for score in user_scores]

	# remove the password
	for score in score_dict:
		score['owner'].pop('password')

	print(score_dict)

	return jsonify(
		data=score_dict,
		message="Succesfully created score",
		status=200
		), 200


# score update route
@scores.route('/<id>', methods=['PUT'])
def update_score(id):
	# get the information from the reques
	payload = request.get_json()
	print(payload)

	# look up score that matches the id
	score = models.Score.get_by_id(id)

	# check if this user is the owner
	if score.owner.id == current_user.id:
		# if it does, then we can proceed

		score.high_score = payload['high_score'] if 'high_score' in payload else None
		score.rank = payload['rank'] if 'rank' in payload else None
		# save the changes
		score.save()

		# convert score to dictionary
		score_dict = model_to_dict(score)
		# remove the password
		score_dict['owner'].pop('password')

		return jsonify(
			data=score_dict,
			message="Succesfully updated score and rank",
			status=200
			), 200
	else: 
		return jsonify(
			data={},
			message="This user is not the owner of this score",
			status=401
			), 401