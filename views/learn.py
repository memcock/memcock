from flask import Blueprint, redirect, url_for, render_template, session, jsonify
from app import app
from lib.template import templated
# from lib.match import getImagePair, shuffleImageSet
from lib.utils import randomOrder
import json

learn_app = Blueprint('learn', __name__)

@learn_app.route('/learn')
@templated('learn.html')
def learn():
	session.modified = True
	if not session.get('game', None):
		print('no game brah')
		return(redirect(url_for('load.setup')))
	if session.get('stage', False) == 'recall':
		print('no stage')
		return redirect(url_for('recall.recall'))
	game = session['game']
	game.beginLearn()
	print(game.__dict__)
	pair = game.current
	print(pair)
	ret = dict(babe = pair.babe.link,
				cock = pair.cock.link,
				minTime = game.minTime,
				maxTime = game.maxTime,
				images = json.dumps(game.images))
	return ret

@learn_app.route('/learn/next')
@templated('learn-images.html')
def nextImage():
	if not session.get('game', False):
		return '', 400
	game = session['game']
	session.modified = True
	pair = game.next
	if pair:
		ret = dict(	babe = pair.babe.link,
					cock = pair.cock.link)
		return ret
	return '', 204
