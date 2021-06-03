from telegram.ext import CommandHandler
from subprocess import call, check_output

def version(update, context):
    version = 'dev'
    if call('git diff-index --quiet HEAD'.split()):
        version = 'dev'
    else:
        if call('git describe --tags --exact-match'.split()) == 0:
            version = check_output('git describe --tags --exact-match'.split()).decode('UTF-8').rstrip()
        else:
            version = check_output('git rev-parse --short HEAD'.split()).decode('UTF-8').rstrip()
    context.bot.send_message(chat_id=update.effective_chat.id, text=version)
version_handler = CommandHandler('version', version)