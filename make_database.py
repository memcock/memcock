#!/usr/bin/python3
import sys
import socket
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from config import config, getLogger
import time

_log = getLogger(__name__)

def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    _log.info("Attempting to connect to %s on port %s"%(address, port))
    try:
        s.connect((address, port))
        _log.info("Connected to %s on port %s"%(address, port))
        return True
    except socket.error as e:
        _log.error("Connection to %s on port %s failed: %s"%(address, port, e))
        return False

print(config.app.DB_PASS)
if __name__ == '__main__':
	for x in range(10):
		if check_server('postgres', 5432):
			dbUri = '%s%s:%s@%s'%(config.app.DB_DRIVER, 
									config.app.DB_USER,
									config.app.DB_PASS,
									config.app.DB_PATH)
			engine = create_engine(dbUri)
			if not database_exists(engine.url):
				_log.info('Database does not exist, creating...')
				create_database(engine.url)
				from app import db
				from models import images, imageSets, stats
				db.create_all()
			else:
				_log.info('Database already exists')
			sys.exit(0)
		else:
			_log.error('Failed to connect to database. Failures: %i'%(x+1))
			time.sleep(5)
	sys.exit(1)