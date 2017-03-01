from app import db
from sqlalchemy.sql import func
import datetime

pairAssoc = db.Table('pair_assoc',
			db.Column('pair_id', db.Integer, db.ForeignKey('image_pair.id')),
			db.Column('set_id', db.Integer, db.ForeignKey('image_set.id'))
			)

class ImageSet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pairs = db.relationship('ImagePair', secondary=pairAssoc,
			backref=db.backref('sets', lazy='joined'), lazy = 'joined')
	last_used = db.Column(db.DateTime(), server_default=func.now())

	def __init__(self, pairs):
		self.pairs.extend(pairs)
		self.last_used = datetime.datetime.utcnow()

	def __repr__(self):
		return '<ImageSet pairs: %s>'%'\n'.join([str(x) for x in self.pairs])

class ImagePair(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	babe_id = db.Column(db.Integer, db.ForeignKey('image.id'))
	babe = db.relationship("Image", foreign_keys=babe_id, lazy = 'joined')
	cock_id = db.Column(db.Integer, db.ForeignKey('image.id'))
	cock = db.relationship("Image", foreign_keys=cock_id, lazy = 'joined')

	def __init__(self, babe, cock):
		self.babe = babe
		self.cock = cock

	def __repr__(self):
		babe = 'babe: %s'%self.babe.fullname
		cock = 'cock: %s'%self.cock.fullname
		return '<ImagePair %s %s>'%(babe, cock)
