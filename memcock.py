from flask import request, render_template, session, redirect, url_for, abort
from app import app
from lib.template import templated
from config import config
import json
import uuid

from views.learn import learn_app
app.register_blueprint(learn_app)

from views.recall import recall_app
app.register_blueprint(recall_app)

from views.load import load_app
app.register_blueprint(load_app)
# RIP
@app.after_request
def clacks_overhead(resp):
	resp.headers.add('X-Clacks-Overhead', 'GNU Terry Pratchett')
	return resp

@app.before_request
def userID():
	if not session.get('user_uuid', False):
		session['user_uuid'] = uuid.uuid4().hex

@app.route('/')
@templated('home.html')
def home():
	return {}


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
