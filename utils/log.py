from os import environ
from logging import getLogger
from weakref import WeakValueDictionary
try:
	from coloredlogs import install
except:
	import logging
	loglevel = getattr(logging, environ['LOGLEVEL']) if 'LOGLEVEL' in environ.keys() else None
	logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=loglevel)
	getLogger('Log').warn("Module coloredlogs load failed, fallback to legacy logging")

_logger_cache = WeakValueDictionary()

def get_logger(name):
	if name not in _logger_cache:
		logger = getLogger(name)
		if 'install' in globals():
			install(logger=logger)
		_logger_cache[name] = logger
	else:
		logger = _logger_cache[name]
	return logger