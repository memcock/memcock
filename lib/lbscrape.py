import requests
import time
from config import config


class LBScrape:
	def __init__(self, endpoint):
		self._endpoint = endpoint

	def _build_create_endpoint(self, subreddit):
		return self._endpoint + '/r/%s'%subreddit

	def _build_queue_endpoint(self, job_id):
		return self._endpoint + '/queue/%s'%job_id
	
	def _build_result_endpoint(self, job_id):
		return self._endpoint + '/result/%s'%job_id

	def _build_check_endpoint(self, subreddit):
		return self._endpoint + '/check/%s'%subreddit

	def _create_job(self, subreddit, count, exclude = []):
		args = dict(wanted=count, exclude = exclude)
		endpoint = self._build_create_endpoint(subreddit)
		resp = requests.get(endpoint, params=args)
		if resp.status_code == 202:
			data = resp.json()
			job_id = data.get('result', dict()).get('uuid', None)
			return job_id
		return None

	def _check_job_status(self, job_id):
		endpoint = self._build_queue_endpoint(job_id)
		resp = requests.get(endpoint)
		if resp.status_code == 303 and resp.json()['result']['complete']:
			return True
		return False

	def _check_subreddit_validity(self, subreddit):
		resp = requests.get(self._build_check_endpoint(subreddit))
		if resp.status_code == 200:
			return resp.json().get('valid', False)
		return False

	def _get_job_results(self, job_id):
		endpoint = self._build_result_endpoint(job_id)
		results = requests.get(endpoint).json()
		links = results['result']['links']
		return links

	def create(self, subreddit, wanted, exclude = []):
		job_id = self._create_job(subreddit, wanted, exclude)
		return Job(self, job_id)

	def status(self, job_id):
		return self._check_job_status(job_id)

	def results(self, job_id):
		return self._get_job_results(job_id)

	def check(self, subreddit):
		return self._check_subreddit_validity(subreddit)

class Job:
	def __init__(self, client, job_id):
		self._client = client
		self._job_id = job_id

	def _get_results(self):
		return self._client.results(self._job_id)

	def _check_status(self):
		return self._client.status(self._job_id)

	@property
	def id(self):
		return self._job_id

	@property
	def status(self):
		return self._check_status()

	@property
	def results(self):
		if self.status:
			return self._get_results()
		return None

	def wait(self, timeout = None, interval = 5):
		if timeout:
			timeout = time.time() + timeout
		while True:
			if self.status:
				return self.results
			if timeout <= time.time():
				raise TimeoutError
			time.sleep(interval)

lbsClient = LBScrape(config.lbscrape.endpoint)

def job_from_id(job_id):
	return Job(lbsClient, job_id)