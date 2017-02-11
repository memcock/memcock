from lib.utils import IDHasher
from models.imageSets import ImageSet, ImagePair
from app import db
import random
import datetime
from lib.database import incrementSubredditHit
from lib.query import getImages

def createImageSet(babes, cocks, babesrc, cocksrc):
	pairs = []
	ids = []
	print(len(babes), len(cocks))
	for x in range(len(babes)):
		p = ImagePair(babes[x], cocks[x])
		db.session.add(p)
		pairs.append(p)
		ids.append(babes[x].fullname)
		ids.append(cocks[x].fullname)
	imageSet = ImageSet(pairs)
	db.session.add(imageSet)
	db.session.commit()
	incrementSubredditHit(babesrc)
	incrementSubredditHit(cocksrc)
	return imageSet, ids


def getImagePair(id, index):
	imageSet = ImageSet.query.get(IDHasher.decode(id))
	imageSet.last_used = datetime.datetime.utcnow()
	return imageSet.pairs[index]

def generateChoices(correct, image_set, subreddit, count = 2):
	others = [x.cock for x in image_set.pairs]
	others = [x for x in others if x.id != correct.cock.id]
	choices = random.sample(others, count)
	choices.append(correct.cock)
	random.shuffle(choices)
	return correct.babe, choices

def checkChoice(index, choice_id, id):
	imageSet = ImageSet.query.get(IDHasher.decode(id))
	if imageSet.pairs[index].cock.id == IDHasher.decode(choice_id)[0]:
		return True
	return False

def shuffleImageSet(id):
	imageSet = ImageSet.query.get(IDHasher.decode(id))
	pairs = imageSet.pairs
	random.shuffle(pairs)
	imageSet.pairs = pairs
	db.session.add(imageSet)
	db.session.commit()
