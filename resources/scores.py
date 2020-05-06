# import our models and blueprint
import models
from flask import Blueprint, request, jsonify
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
		owner=payload['owner'],
		high_score=payload['high_score'],
		rank=payload['rank']
		)

	score_dict = model_to_dict(new_score)

	return jsonify(
		data=score_dict,
		message="Succesfully created score",
		status=200
		), 200


# score create route
@scores.route('/', methods=['GET'])
def get_score():
	# get the information from the reques
	payload = request.get_json()
	print(payload)

	# create the score
	user_score = models.Score.get(models.Score.owner == payload['owner'])
	print("printing user_score")
	print(user_score)

	score_dict = model_to_dict(user_score)

	return jsonify(
		data=score_dict,
		message="Succesfully created score",
		status=200
		), 200