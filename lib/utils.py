from hashids import Hashids
from config import config
import hashlib
import random

def SRCHasher(src):
	return None

def randomOrder(len):
	items = [ x for x in range(len)]
	random.shuffle(items)
	return items

def extractLink(submission):
	if getattr(submission, 'preview', False):
		width = submission.preview['images'][0]['source']['width']
		height = submission.preview['images'][0]['source']['height']
		if height > width and width > 500 and height > 500 :
			return submission.preview['images'][0]['source']['url']
	return None
