from telegram.ext import CommandHandler
from utils import database

def stats(update, context):
    num = database.stats('users')
    text = "咱总共见过{num}个人啦".format(num=num)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
stats_handler = CommandHandler('stats', stats)