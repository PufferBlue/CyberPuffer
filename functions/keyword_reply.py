from telegram.ext import MessageHandler, Filters
from functions import luck, keyword
from utils import database
from datetime import datetime

def keyword_reply(update, context):
    if (update.message is not None):
        database.query(update.effective_user.id, 'role')
        # Special commands detection
        if update.message.text.startswith("/"):
            if update.message.text.startswith("/luck"):
                arg = update.message.text.partition(' ')
                if arg[2] == '':
                    name = update.effective_user.first_name
                    if update.effective_user.last_name is not None:
                        name += update.effective_user.last_name
                else:
                    name = arg[2]
                luck_text = luck.get_luck_v2(update.effective_user.id, datetime.now(), name)
                context.bot.send_message(chat_id=update.effective_chat.id, text=luck_text)
        reply = keyword.reply(update.message.text)
        if reply.type is not None:
            # Filter mismatched replys
            if update.message.text.startswith("/") ^ reply.match.startswith("/"):
                return
            if reply.type == 'forward':
                context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=reply.from_chat_id, message_id=reply.message_id)
            elif reply.type == 'plaintext':
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply.text)
            elif reply.type == 'sticker':
                context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=reply.sticker_id)
            else:
                pass
keyword_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.regex('^/[luck|lottery|caffeine|caculate]'), keyword_reply)