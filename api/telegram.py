from utils.log import get_logger
logger = get_logger(name='Telegram')

try:
	from telegram import constants, __version__ as ptb_version
	from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
except:
	logger.error("Load PTB module failed")

class BotHandler:

	def __init__(self, config, proxy=None):
		self._bot_id, api_secret, self._config_path = config.split(':')
		request_kwargs = {'proxy_url': proxy} if proxy is not None else None
		self._updater = Updater(token=self._bot_id + ':' + api_secret, use_context=True, request_kwargs=request_kwargs)
		self._dispatcher = self._updater.dispatcher
		self._module_path = 'modules/'

	def _get_config(self, config_path):
		try:
			try:
				config_id = int(config_path)
				from tomli import loads
				channel_info = self._dispatcher.bot.get_chat(config_id)
				if channel_info.pinned_message is not None:
					index = channel_info.pinned_message
					return loads(index.text)
				else:
					raise LookupError
			except ValueError:
				try:
					from tomli import load
					with open(config_path, encoding="utf-8") as f:
						return load(f)
				except:
					raise LookupError
		except:
			return None

	def init(self):
		from os import scandir
		self._config = self._get_config(self._config_path)
		with scandir(self._module_path) as it:
			for entry in it:
				if entry.is_file():
					self._load_func(entry.path)

	def start(self):
		from distutils.version import LooseVersion
		if LooseVersion(ptb_version) >= LooseVersion('13.5'):
			self._updater.start_polling(allowed_updates=constants.UPDATE_ALL_TYPES)
		else:
			logger.warn('PTB version < 13.5, not all update types are listening')
			self._updater.start_polling()

	def stop(self):
		self._updater.stop()

	def send_message(self, message, receiver):
		if 'type' in receiver.keys():
			if receiver['type'] == 'text':
				reply = self._dispatcher.bot.send_message(chat_id=receiver["user_id"], text=message)
			elif receiver['type'] == 'sticker':
				reply = self._dispatcher.bot.send_sticker(chat_id=receiver["user_id"], sticker=message)
			elif receiver['type'] == 'forward':
				from_chat_id, sep, message_id = message.partition('@')
				reply = self._dispatcher.bot.forward_message(chat_id=receiver["user_id"], from_chat_id=from_chat_id, message_id=message_id)
			else:
				pass
		else:
			reply = self._dispatcher.bot.send_message(chat_id=receiver["user_id"], text=message)
		return reply

	def _find_func(self, name):
		default_func_group = self._dispatcher.handlers[0]
		for func in default_func_group:
			if func.callback.__name__ == name:
				return func

	def _wrap_func(self, func, name):
		def wrapped_func(update, context):
			from json import dumps
			data = {
				'message': update.message.text,
				'sender': {
			    	"user_id": update.effective_chat.id,
			    	"source": 'telegram@'+self._bot_id,
			    	"config": self._config
			    }
			}
			result =  func(data = data)
			if result is not None:
				reply = self.send_message(result['message'],result['receiver'])
				return reply
			else:
				return None
		if name == 'keyword':
			return MessageHandler(Filters.text & (~Filters.command), wrapped_func)
		else:
			return CommandHandler(name, wrapped_func)

	def _load_func(self, filepath):
		try:
			from zipimport import zipimporter
			module = zipimporter(filepath).load_module('__main__')
			funcname = module.__command__
			handler = self._wrap_func(module.main, funcname)
			self._dispatcher.add_handler(handler)
			logger.info('Module {} loaded'.format(funcname))
		except:
			from traceback import print_exc
			print_exc()
			logger.warning('Module {} failed to load'.format(funcname))

	def _unload_func(self, name):
		handler = self._find_func(self._dispatcher,name)
		if handler is not None:
			self._dispatcher.remove_handler(handler)
			logger.info('Module {} unloaded'.format(name))
			return True
		else:
			logger.warning('{} failed to unload'.format(name))
			return False

	def _list_func(self):
		default_func_group = self._dispatcher.handlers[0]
		func_list = [handler.callback.__name__ for handler in default_func_group]
		return func_list