from app import db
from sqlalchemy.sql import func
import datetime


class SubReddit(db.Model):
	source = db.Column(db.Text, primary_key = True)
	hits = db.Column(db.Integer, unique=False, default = 0)
	last_used = db.Column(db.DateTime(), server_default=func.now())
	scan_start = db.Column(db.Integer, default = 0)
	scan_end = db.Column(db.Integer)

	def __init__(self, source):
		self.source = source

	def updateLastUsed(self):
		self.last_used = datetime.datetime.utcnow()
		self.hits = self.hits + 1
		db.session.add(self)
		db.session.commit()

	def updateScan(self, start = None, end = None):
		if start:
			self.scan_start = start
		if end:
			self.scan_end = end
		if start or end:
			db.session.add(self)
			db.session.commit()
