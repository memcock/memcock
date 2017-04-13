from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import configDict as config
import os
import redis
from flask_kvsession import KVSessionExtension
from simplekv.decorator import PrefixDecorator
from simplekv.memory.redisstore import RedisStore
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)

store = RedisStore(redis.StrictRedis(host = 'redis', db = 1))
prefixed_store = PrefixDecorator('sessions_', store)
KVSessionExtension(store, app)
if config.get('app', False):
	app.config.update(**config['app'])
	app.config['DEBUG'] = True

# create Database
if config.get('app', {}).get('DB_PATH', False):
	dbpath = '%s%s:%s@%s'%(config['app']['DB_DRIVER'],
							config['database']['user'],
							config['database']['password'],
							config['app']['DB_PATH'])
	# dbpath = config['app']['DB_URI'] + config['app']['DB_PATH']
	print(dbpath)
	app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
	db = SQLAlchemy(app)
