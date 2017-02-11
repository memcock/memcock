from app import db
from models.images import Image
from models.imageSets import ImageSet
from models.stats import SubReddit
from lib.utils import IDHasher
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from config import getLogger
_log = getLogger(__name__)

def getImages(src, shuffle = True):
	if shuffle:
		return Image.query.filter_by(src = src).order_by(func.random()).all()
	return Image.query.filter_by(src = src).all()

def getImageSet(id):
	return ImageSet.query.get(IDHasher.decode(id))

def getSubReddit(subreddit, create = True):
	subreddit = subreddit.lower()
	s = SubReddit.query.get(subreddit)
	if not s and create:
		s = SubReddit(subreddit)
		try:
			db.session.add(s)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			return getSubReddit(subreddit, create)
	return s

def addImage(link, sub, fullname):
	img = Image(link, sub, fullname)
	try:
		db.session.add(img)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return None
	return img

def insertImages(links):
	images = [addImage(link['url'], link['subreddit'], link['fullname']) for link in links]
	return images


def incrementSubredditHit(sub):
	s = getSubReddit(sub)
	s.updateLastUsed()

def getPopular(limit=5):
	popular = SubReddit.query.order_by(SubReddit.hits.desc()).limit(limit).all()
	return [(x.source, x.hits) for x in popular]
