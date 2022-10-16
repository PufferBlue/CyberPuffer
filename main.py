from argparse import ArgumentParser
from os import environ
from sys import argv
from itertools import chain

__version__ = 'dev'

def main():
	# Initialising Argument Parser
	parser = ArgumentParser(prog='CyberPuffer', description='CyberPuffer - Just yet another telegram bot')
	parser.add_argument('--config', '-c', dest='api_config', help='api config for the bot', action='append', metavar='', required=True)
	parser.add_argument('--proxy', '-x', dest='proxy', help='use provided proxy', metavar='')
	parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='enable debug messages')
	parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

	# Read Environment Varibles
	if 'API_CONFIG' in environ.keys():
		all_args = chain([a for b in environ['API_CONFIG'].splitlines() for a in ('-c', b)], argv[1:])
	else:
		all_args = argv[1:]

	# Parse Argument
	args = parser.parse_args(args=all_args)

	# Setup Logging Level
	if args.verbose:
		environ["LOGLEVEL"] = "DEBUG"
		environ["COLOREDLOGS_LOG_LEVEL"] = "DEBUG"

	# Start Jobs
	from utils.jobs import start_jobs
	start_jobs(args)

if __name__ == "__main__":
	main()