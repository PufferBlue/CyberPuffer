from telegram.ext import Updater
from telegram import constants
from utils import config, log, database
from functions import *

logger = log.get_logger(name = 'Bot')
database.check_database()
REQUEST_KWARGS={'proxy_url': config.proxy_url}
updater = Updater(token=config.telegram_api_secret, use_context=True, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
updater.start_polling(allowed_updates=constants.UPDATE_ALL_TYPES)
logger.warning('Bot started')

enabled_funcs = [
    (uptime,uptime.uptime_handler),
    (stats, stats.stats_handler),
    (antispam, antispam.channel_handler),
    (keyword_reply, keyword_reply.keyword_handler)
    ]

for func, handler in enabled_funcs:
    dispatcher.add_handler(handler)
    logger.warning('{} loaded'.format(func.__name__))