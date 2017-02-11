from app import db
from models.images import Image
from lib.query import getImages as GetImagesFromReddit
from lib.database import getImages as GetImagesFromDB

class ImagePool:
	def __init__(self, subreddit, used = []):
		self._subreddit = subreddit
		self._pool = []
		self._low_watermark = 10
		self._pulledFromDB = False
		self._usedImages = used[:]

	def _checkPoolLevel(self):
		return len(self._pool) > self._low_watermark

	def _getFromPool(self):
		self._fillPool()
		if self._pool:
			item = self._pool.pop()
			return item
		return self._getFromPool()

	def _fillPool(self, chunk = 10):
		if not self._pulledFromDB:
			self._fillFromDB()
			self._pulledFromDB = True
		if not self._checkPoolLevel():
			self._fillFromReddit(chunk)

	def _fillFromReddit(self, chunk):
		for image in GetImagesFromReddit(self._subreddit, chunk, self._usedImages):
			self._pool.append(image)
			chunk = chunk - 1
			if chunk == 0:
				break

	def _fillFromDB(self):
		for image in GetImagesFromDB(self._subreddit):
			self._pool.append(image)

	def _getImage(self):
		image = self._getFromPool()
		if not image.id in self._usedImages:
			self._usedImages.append(image.id)
			image.updateLastUsed()
			return image
		return self._getImage()

	def get(self, count):
		while count > 0:
			yield self._getImage()
			count = count - 1

	def getList(self, count):
		urls = []
		for u in self.get(count):
			urls.append(u)
		return urls
