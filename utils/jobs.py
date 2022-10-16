from utils.log import get_logger
from weakref import WeakValueDictionary
from traceback import print_exc

logger = get_logger(name='Jobs')
handler_list = WeakValueDictionary()

def start_jobs(args):
	for api_item in args.api_config:
		name, _, config = api_item.strip().partition(':')
		if name == 'telegram':
			logger.info("Starting telegram job")
			try:
				from api.telegram import BotHandler
				telegram_handler = BotHandler(config, proxy=args.proxy)
				telegram_handler.init()
				telegram_handler.start()
			except:
				logger.error("Telegram job start failed")
				print_exc()
				continue