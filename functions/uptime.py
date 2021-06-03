from telegram.ext import CommandHandler
from time import monotonic
from utils import globals
from humanfriendly import format_timespan

def uptime(update, context):
    time_now = monotonic() 
    time_text = format_timespan(int(time_now - globals.time_start))\
        .replace('years','年').replace('year','年')\
        .replace('months','月').replace('month','月')\
        .replace('days','日').replace('day','日')\
        .replace('hours','小时').replace('hour','小时')\
        .replace('minutes','分钟').replace('minute','分钟')\
        .replace('seconds','秒').replace('second','秒')\
        .replace('and ','').replace(',','')
    text = "咱已经正常运行了 {}".format(time_text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
uptime_handler = CommandHandler('uptime', uptime)