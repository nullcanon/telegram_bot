#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
# -*- coding: UTF-8 -*-

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from decimal import Decimal
import json
import httpx
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown
import command_approve_check, command_bee_check, command_help, command_start

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def loadConfig():
    with open("./config.json","r") as f:
        load_dict = json.load(f)
    return load_dict

config = loadConfig()
GOAPIKEY = config['go_plus_api_key']
GOAPISECRECT = config['go_plus_api_secrect']
BOTAPIKEY =  config['bot_api_key']
CHANNEL = config['token_check_channel_id']

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=BOTAPIKEY, request_kwargs={'proxy_url': 'http://192.168.1.34:1080/'})

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(command_start.handler)
    dispatcher.add_handler(command_help.handler)
    dispatcher.add_handler(command_bee_check.handler)
    dispatcher.add_handler(command_approve_check.handler)

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_check_token))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()