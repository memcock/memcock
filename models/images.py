from app import db
import uuid
import hashlib
from sqlalchemy.sql import func
import datetime
from config import config

class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.Text)
	link = db.Column(db.Text)
	hits = db.Column(db.Integer, unique=False)
	src = db.Column(db.String(32))
	last_used = db.Column(db.DateTime(), server_default=func.now())
	stock = db.Column(db.Integer)

	def __init__(self, link, src, fullname):
		self.link = link
		self.hits = 0
		self.src = src
		if not src == config.images.babes and not src == config.images.cocks:
			self.stock = 0
		else:
			self.stock = 1
		self.fullname = fullname

	def updateLastUsed(self):
		self.last_used = datetime.datetime.utcnow()
		self.hits = self.hits + 1
		db.session.add(self)
		db.session.commit()

	def __repr__(self):
		return '<Image %s>'%self.fullname
