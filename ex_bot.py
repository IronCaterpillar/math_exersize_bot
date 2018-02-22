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
from telegram import *
from random import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
exercise_result=0
exercise_str=""
settings_dict={}


def get_minus_exercise():
    a=1+int(random()*30)
    b=1+int(random()*(a-1))
    return a-b,str(a)+"-"+str(b)+"="

def get_plus_exercise():
    a=1+int(random()*30)
    b=1+int(random()*(a-1))
    return a+b,str(a)+"+"+str(b)+"="

def new_question(bot,update):
    check_new_chat(bot, update)
    settings = settings_dict[update.message.chat.id]
    settings["result"],settings["exercise_str"] = settings["func"]()
    
def ask_question(bot,update):
    check_new_chat(bot, update)
    settings = settings_dict[update.message.chat.id]
    update.message.reply_text("Exercise: "+settings["exercise_str"])

def check_result(bot,update):
    if check_new_chat(bot, update):
        ask_question(bot,update)
    else:
        settings = settings_dict[update.message.chat.id]
        result_ok = False
        try:
            cur_answer=int(update.message.text)
            if cur_answer==settings["result"]:result_ok=True
        except: pass
        if result_ok: 
            update.message.reply_text("😺 Perfect!")
            new_question(bot,update)
        else:
            update.message.reply_text("😿 Try again")
        ask_question(bot,update)
            
    

def send_keyboard(bot, update):
    custom_keyboard = [[KeyboardButton(text="/Minus")],[KeyboardButton(text="/Plus")]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat.id, text="Check an exercise", reply_markup=reply_markup)

def check_new_chat(bot, update):
    if update.message.chat.id not in settings_dict:
        new_settings = {}
        settings_dict[update.message.chat.id]=new_settings
        new_settings["func"] = lambda: -1,"Please select exercise type!"
        new_settings["result"]=0
        new_settings["exercise_str"]=""
        return True
    return False
    
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    global settings_dict    
    send_keyboard(bot, update)
    update.message.reply_text("Please select exercise type!")
       

def plus_pressed(bot, update):
    check_new_chat(bot, update)
    settings = settings_dict[update.message.chat.id]
    settings["func"] = get_plus_exercise 
    new_question(bot,update)
    ask_question(bot,update)

def minus_pressed(bot, update):
    check_new_chat(bot, update)
    settings = settings_dict[update.message.chat.id]    
    settings["func"] = get_minus_exercise
    new_question(bot,update)
    ask_question(bot,update)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    if check_new_chat(bot, update):
        ask_question(bot,update)
    else:
           check_result(bot,update)


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
    dp.add_handler(CommandHandler('Plus', plus_pressed))
    dp.add_handler(CommandHandler('Minus', minus_pressed))
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
