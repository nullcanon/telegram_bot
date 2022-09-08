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
import time
import hashlib


def loadConfig():
    with open("./config.json","r") as f:
        load_dict = json.load(f)
    return load_dict

config = loadConfig()
BOTAPIKEY =  config['bot_api_key']
CHANNEL = config['token_check_channel_id']
KEY = config['information_key']


def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

content_send = {}

def getMessages():
    messages = []
    url = "https://www.maitanbang.com/api/news/index?key=" + KEY
    result = httpx.get(url, timeout = 10)
    result_json = json.loads(result.text)
    if result_json['code'] != 200:
        return messages
    datas = result_json['data']
    for data in datas:
        content = data['content']
        md5 = string_to_md5(content)
        if content_send[md5] not True:
            messages.append(content)
            content_send[string_to_md5(content)] = True
    # messages = ["【Optimism：以太坊合并时不会暂停网络，资产仅可提取到PoS链上】MarsBit消息，以太坊二层扩容网络 Optimism 在其社交平台表示，以太坊合并将不会对 Optimism 网络造成影响，不会暂停网络，存取款可照常进行。一旦合并触发，Optimism 的运营将完全转移到以太坊 PoS 链上，Optimism 上的资产也将只能提取到 PoS 链上。"]
    return messages

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=BOTAPIKEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_check_token))
    while True:
        try:
            messages = getMessages()
            for message in messages:
                updater.bot.send_message(chat_id = CHANNEL, text = message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                time.sleep(2)
            time.sleep(60)
        except:
            continue

    # Start the Bot
    updater.start_polling(10)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()