from models.imageSets import ImageSet
import random
from flask import session
from lib.match import generateChoices, createImageSet

class Game:
	def __init__(self, babesrc = None, cocksrc = None, pairs = 15, minTime = 0, maxTime = 0, used = [], **kwargs):
		self.babesrc = babesrc.lower()
		self.cocksrc = cocksrc.lower()
		self.pairs = int(pairs)
		self.order = [x for x in range(self.pairs)]
		self.minTime = int(minTime)
		self.maxTime = int(maxTime)
		self.shuffle_order = False
		self.used = list(used)
		self.index = 0
		self.set_id = None

		self.shuffle_on_failure = kwargs.get('shuffle_on_failure', 'off')
		self.shuffle_on_failure = self.shuffle_on_failure.lower() == 'on'
		self.shuffle_always = kwargs.get('shuffle_always', 'off')
		self.shuffle_always = self.shuffle_always.lower() == 'on'
		self.increase_max = int(kwargs.get('increase_max', False))
		self.increase_min = int(kwargs.get('increase_min', False))
		self.failure_mode = kwargs.get('failure_mode', 'learning')

	def onFailure(self):
		self.index = 0
		self.minTime = self.minTime + self.increase_min
		self.maxTime = self.maxTime + self.increase_max
		if self.shuffle_on_failure or self.shuffle_always:
			self._shuffle()

	def onSuccess(self):
		pass

	def beginLearn(self):
		if self.shuffle_always:
			self._shuffle()

	def beginRecall(self):
		if self.shuffle_always:
			self._shuffle()

	def _shuffle(self):
		random.shuffle(self.order)

	def check(self, fullname):
		if self.current.cock.fullname == fullname:
			return True
		self.onFailure()
		return False

	def update(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

		self.pairs = int(self.pairs)
		self.order = [x for x in range(self.pairs)]
		self.minTime = int(self.minTime)
		self.maxTime = int(self.maxTime)
		self.increase_max = int(self.increase_max)
		self.increase_min = int(self.increase_min)
		self.shuffle_on_failure = self.shuffle_on_failure == 'on'
		self.shuffle_always = self.shuffle_always == 'on'
		self.index = 0

	@property
	def current(self):
		if self.set_id:
			return self.image_set.pairs[self.order[self.index]]
		return None

	@property
	def next(self):
		if self.index < self.pairs - 1:
			self.index = self.index + 1
			return self.current
		self.index = 0
		return None

	@property
	def image_set(self):
		if not getattr(self, 'image_set_obj', False) or self.image_set_obj.id != self.set_id:
		 	self.image_set_obj = ImageSet.query.get(self.set_id)
		return self.image_set_obj

	@property
	def choices(self):
		return generateChoices(self.current, self.image_set, self.cocksrc)
	
	@property
	def images(self):
		imgs = []
		for pair in self.image_set.pairs:
			imgs.append(pair.babe.link)
			imgs.append(pair.cock.link)
		return imgs


def buildGame(game, babes, cocks):
	imageSet, used = createImageSet(babes, cocks, game.babesrc, game.cocksrc)
	game.set_id = imageSet.id
	game.used = game.used + used
	return game
