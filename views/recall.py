from flask import Blueprint, redirect, url_for, session
from app import app
from lib.template import templated
from lib.match import generateChoices, checkChoice, shuffleImageSet
import json
from lib.utils import randomOrder

recall_app = Blueprint('recall', __name__)

@recall_app.route('/recall')
@templated('recall.html')
def recall():
	session.modified = True
	if not session.get('game', False):
		return '', 400
	game = session['game']
	game.beginRecall()
	correct, choices = game.choices
	ret = {
		'babe': correct.link,
		'cocks': choices,
		'failure_mode': game.failure_mode
	}
	return ret

@recall_app.route('/recall/next')
@templated('recall-images.html')
def recallNext():
	session.modified = True
	if not session.get('game', False):
		return '', 400
	game = session['game']
	correct, choices = game.choices
	ret = {
		'babe':correct.link,
		'cocks': choices
	}
	return ret

@recall_app.route('/recall/check/<choice>')
def checkMatch(choice):
	session.modified = True
	if not session.get('game', False):
		print('Failed for: No Game')
		return '', 406
	game = session['game']
	if game.check(choice):
		if game.next:
			return '', 200
		return '', 204
	print('Failed for: Incorrect Choice')
	return '', 406

@recall_app.route('/recall/failure')
@templated('fail-modal.html')
def failure():
	return {}

@recall_app.route('/recall/success')
@templated('success-modal.html')
def finished():
	return '', 204
