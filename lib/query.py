from config import config, getLogger
from lib.database import addImage, getSubReddit
from lib.lbscrape import lbsClient
import time

moduleLogger = getLogger(__name__)


def getPosts(subreddit, start = None, end = None):
	args = dict(wanted=count)
	resp = requests.get(config.lbscrape.address + '/r/%s'%subreddit, params=args)
	if resp.status_code == 202:
		job_id = resp.json()['result']['uuid']
		while True:
			resp = requests.get(config.lbscrape.address + '/queue/%s'%job_id)
			if resp.status_code == 303:
				results = requests.get(config.lbscrape.address + '/result/%s'%job_id).json()
				return results['result']['links']
			time.sleep(5)

def getImageLinks(subreddit, count, exclude = []):
	job = lbsClient.create(subreddit, count, exclude)
	if job:
		return job.id
	return False

def getImages(subreddit, count, exclude = []):
	job = lbsClient.create(subreddit, count, exclude)
	links = job.wait()
	print(links)
	images = [addImage(link['url'], subreddit, link['fullname']) for link in links]
	images = [x for x in images if x]
	return images

def checkSubreddit(sub):
	moduleLogger.debug('Checking subreddit %s for validity'%sub)
	if not getSubReddit(sub, create = False):
		 return lbsClient.check(sub)
	return True