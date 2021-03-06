from telegram import constants
from telegram.ext import Updater
from distutils.version import LooseVersion
from telegram import __version__ as ptb_version
from utils import functions, globals, log
logger = log.get_logger(name='Bot')

def polling(args):

    request_kwargs = {
        'proxy_url': args.proxy} if args.proxy is not None else None
    updater = Updater(token=args.api_secret, use_context=True,
                      request_kwargs=request_kwargs)
    dispatcher = updater.dispatcher
    globals.dispatcher = dispatcher
    functions.load_all_funcs(dispatcher, args)
    if LooseVersion(ptb_version) >= LooseVersion('13.5'):
        updater.start_polling(allowed_updates=constants.UPDATE_ALL_TYPES)
    else:
        logger.warn('PTB version < 13.5, not all update types are listening')
        updater.start_polling()