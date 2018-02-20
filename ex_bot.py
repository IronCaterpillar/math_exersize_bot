#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from random import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
exersize_result=0
exersize_str=""


def get_minus_exersize():
    a=1+int(random()*30)
    b=1+int(random()*(a-1))
    return a-b,str(a)+"-"+str(b)+"="

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    global exersize_result
    global exersize_str
    exersize_result,exersize_str = get_minus_exersize()
    update.message.reply_text("Пример: "+exersize_str)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    global exersize_result,exersize_str
    local_result=0
    try:
        local_result=int(update.message.text)
    except:
        local_result=0        
        
    if exersize_result==local_result:
        update.message.reply_text("Правильно, молодец! :)")
        exersize_result,exersize_str = get_minus_exersize()
        update.message.reply_text("Пример: "+exersize_str)
        
    else:
        update.message.reply_text("Неправильно! :(")
        update.message.reply_text("Попробуй ещё: "+exersize_str)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("426671202:AAHXwrcGVs10aXnM_nvySTPXkX0fOxL3knE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
