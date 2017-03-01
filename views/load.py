from flask import Blueprint, redirect, url_for, render_template, session, request, jsonify
from app import app
from lib.template import templated
from lib.match import createImageSet
from config import config
from lib.game import Game, buildGame
from lib.query import checkSubreddit, getImageLinks
from lib.database import getPopular, insertImages
from lib.lbscrape import job_from_id
load_app = Blueprint('load', __name__)

@load_app.route('/load', methods = ['POST'])
def loadImages():
	session.modified = True
	args = {}
	for pair in request.get_json():
		args[pair['name']] = pair['value']
	if not checkSubreddit(args['babesrc']):
		return jsonify(success = False, error='%s does not exist!'%args['babesrc'])
	elif not checkSubreddit(args['cocksrc']):
		return jsonify(success = False, error='%s does not exist!'%args['cocksrc'])
	used = session.get('used_pics', [])
	session['game_args'] = args
	game = session.get('game', None)
	if not game:
		game  = Game(**args)
	else:
		game.update(**args)
		session['game'] = game

	session['cock_job_id'] = getImageLinks(game.cocksrc, game.pairs, used)
	session['babe_job_id'] = getImageLinks(game.babesrc, game.pairs, used)
	session['stage'] = 'learn'
	session['order'] = False
	return jsonify(success = True)

@load_app.route('/load/status')
def status():
	session.modified = True
	cock_id = session.get('cock_job_id', None)
	babe_id = session.get('babe_job_id', None)
	babe_job = job_from_id(babe_id)
	cock_job = job_from_id(cock_id)
	if babe_job.status and cock_job.status:
		babe_links = babe_job.results
		cock_links = cock_job.results
		babes = insertImages(babe_links)
		cocks = insertImages(cock_links)
		game = Game(**session['game_args'])
		session['game'] = buildGame(game, babes, cocks)
		used = session.get('used_pics', [])
		session['used_pics'] = used + game.used
		return jsonify(success = True)
	return jsonify(success = False)

@load_app.route('/load/config')
@templated('config.html')
def setup():
	session.modified = True
	game = session.get('game', None)
	options = {
		'minTime' : 0,
		'maxTime' : 0,
		'pairs' : config.images.setSize,
		'babesrc' : config.images.babes,
		'cocksrc' : config.images.cocks,
		'popular' : getPopular(),
		'suggest' : [x[0] for x in getPopular(limit=10)],
		}
	if game:
		options.update({
			'minTime' : game.minTime,
			'maxTime' : game.maxTime,
			'pairs' : game.pairs,
			'babesrc' : game.babesrc,
			'cocksrc' : game.cocksrc,
			})
	return options
