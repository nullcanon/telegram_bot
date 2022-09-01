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
from web3 import Web3
import json
from decimal import Decimal
import httpx
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown

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

def getTokenInfo(token, apikey = GOAPIKEY, apisecrect = GOAPISECRECT):
        params = {'api-key': apikey,
           'api-secrect:': apisecrect}
        params["contract_addresses"] = token
        result = httpx.get('https://api.gopluslabs.io/api/v1/token_security/56', params = params)
        return json.loads(result.text)

        # with open("./example.json", 'r') as f:
        #     temp = json.loads(f.read())
        # return temp

def getAddress(text):
    index = text.find('0')
    if index == -1:
        return ""
    address = text[index:]
    if not Web3.isAddress(address):
        return ""
    return address

    
def buildMessage(input):
    message = \
"*{}（{}）*\n\
*总发行量：*{}\n\
*持有人数：* {}\n\
*可增发：*{}\n\
*买入滑点：*{}%    *卖出滑点：* {}%\n\
*转账开关：*{}     *滑点更改：*{}\n\
*隐藏权限：*{}     *外部调用：*{}\n\
*允许购买：*{}     *允许出售：*{}\n\
*代理合约：*{}     *蜜        獾： *{}\n\
*白名单：    *{}     *黑名单：     *{}\n\
*最大池子：*{}\n\
*所有者：*{}\n\
*代币持仓：*{}\n\
*LP持仓：*{}\n\
"

    # 名称
    name = input['token_name']
    symbol = input['token_symbol']

    # 买入
    buy_tax = "未知"
    if "buy_tax" in input:
        buy_tax = '%.2f'%(float(input['buy_tax']) * 100)

    # 卖出
    sell_tax = "未知"
    if "sell_tax" in input:
        sell_tax = '%.2f'%(float(input['sell_tax']) * 100)

    # 持有人数
    holder = input['holder_count']

    # 总发行量
    supply = '%.2f'%(float(input['total_supply']))

    #转账开关
    transfer_pausable = "未知"
    if "transfer_pausable" in input:
        transfer_pausable = input["transfer_pausable"]
        if transfer_pausable == "0" :
            transfer_pausable = "🟢无"
        else:
            transfer_pausable = "⚠️有"

    #滑点更改
    slippage_modifiable = "未知"
    if "slippage_modifiable" in input:
        slippage_modifiable = input["slippage_modifiable"]
        if slippage_modifiable == "0" :
            slippage_modifiable = "🟢否"
        else:
            slippage_modifiable = "⚠️可"

    #所有者
    owner = input["owner_address"]
    if owner == "0x0000000000000000000000000000000000000000":
        owner = "🟢权限已丢弃"

    #隐藏权限
    hidden_owner = "未知"
    if "hidden_owner" in input:
        hidden_owner = input["hidden_owner"]
        if hidden_owner == "0" :
            hidden_owner = "🟢无"
        else:
            hidden_owner = "⚠️有"


    #外部调用
    external_call = "未知"
    if "external_call" in input:
        external_call = input["external_call"]
        if external_call == "0":
            external_call = "🟢无"
        else:
            external_call = "⚠️有"

    #允许购买
    cannot_buy = "未知"
    if "cannot_buy" in input:
        cannot_buy = input["cannot_buy"]
        if cannot_buy == "0":
            cannot_buy = "🟢可"
        else:
            cannot_buy = "⚠️否"

    #允许出售
    cannot_sell_all = "未知"
    if "cannot_sell_all" in input:
        cannot_sell_all = input["cannot_sell_all"]
        if cannot_sell_all == "0":
            cannot_sell_all = "🟢可"
        else:
            cannot_sell_all = "⚠️否"
    
    #代理合约
    is_proxy = "未知"
    if "is_proxy" in input:
        is_proxy =  input["is_proxy"]
        if is_proxy == "0":
            is_proxy = "🟢否"
        else:
            is_proxy = "⚠️是"

    #蜜獾
    is_honeypot = "未知"
    if "is_honeypot" in input:
        is_honeypot = input["is_honeypot"]
        if is_honeypot == "0":
            is_honeypot = "🟢否"
        else:
            is_honeypot = "❗️是"

    #可增发
    is_mintable = "未知"
    if "is_mintable" in input:
        is_mintable = input["is_mintable"]
        if is_mintable == "0":
            is_mintable = "🟢否"
        else:
            is_mintable = "⚠️可"

    #白名单
    is_whitelisted = "未知"
    if "is_whitelisted" in input:
        is_whitelisted = input["is_whitelisted"]
        if is_whitelisted == "0":
            is_whitelisted = "🟢无"
        else:
            is_whitelisted = "⚠️有"

    #黑名单
    is_blacklisted = "未知"
    if "is_blacklisted" in input:
        is_blacklisted = input["is_blacklisted"]
        if is_blacklisted == "0":
            is_blacklisted = "🟢无"
        else:
            is_blacklisted = "⚠️有"

    #最大池子
    dexs = input["dex"]
    max_dex = "⚠️无"
    max_liquidity = 0
    pair = ""
    for pool in dexs:
        if float(pool["liquidity"]) > max_liquidity:
            max_dex = pool["name"]
            pair = pool["pair"].lower()
            max_liquidity = float(pool["liquidity"])


    #代币持仓
    holders = input["holders"]
    token_lock = "\n销毁占比：{}\n池子占比：{}\n{}"
    destroy = "无"
    pool_amount = "无"
    lock = ""
    for info in holders:
        if info["is_locked"] == 1 and info["address"] == "0x000000000000000000000000000000000000dead":
            t = float(info["balance"]) / float(supply) * 100
            destroy = '%.2f'%t + "%"
            
        if info["is_locked"] == 1 and "locked_detail" in info:
            lock = info["tag"] + "："
            for locked_detail in info["locked_detail"]:
                lock  = lock + "(\n锁定数量：" + '%.2f'%float(locked_detail["amount"]) \
                + ",\n开始时间：" + locked_detail["opt_time"] \
                + ",\n结束时间：" + locked_detail["end_time"] + "  )"
        if info["is_contract"] == 1 and info["address"].lower() == pair:
            t = float(info["balance"]) / float(supply) * 100
            pool_amount = '%.2f'%t + "%"\
                + " (" + info["tag"] + ")"

    token_lock = token_lock.format(destroy, pool_amount, lock)



    #池子持仓
    lp_total_supply = input["lp_total_supply"]
    lp_holders = input["lp_holders"]
    lp_lock = "\n销毁占比：{}\n{}"
    destroy = "无"
    lock = ""
    for info in lp_holders:
        if info["is_locked"] == 1 and info["address"] == "0x000000000000000000000000000000000000dead":
            t = float(info["balance"]) / float(lp_total_supply) * 100
            destroy = '%.2f'%t + "%"

        if info["is_locked"] == 1 and "locked_detail" in info:
            lock = info["tag"] + "："
            for locked_detail in info["locked_detail"]:
                lock  = lock + "(\n锁定数量：" + locked_detail["amount"] \
                + ",\n开始时间：" + locked_detail["opt_time"] \
                + ",\n结束时间：" + locked_detail["end_time"] + "  )"

    lp_lock = lp_lock.format(destroy, lock)

    message = message.format(name, symbol, supply,  holder,is_mintable, buy_tax, 
        sell_tax, transfer_pausable, slippage_modifiable, hidden_owner,external_call,
        cannot_buy, cannot_sell_all, is_proxy, is_honeypot, is_whitelisted, is_blacklisted,
        max_dex, owner, token_lock, lp_lock)
    return message




# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # update.message.reply_markdown_v2(
    #     fr'Hi {user.mention_markdown_v2()}\!',
    #     reply_markup=ForceReply(selective=True),
    # )


def help_command(update: Update, context: CallbackContext) -> None:
    HELP_TEXT = (
        """
        蜜蜂查币由 [BEECapital](https://beecapital.org/) 开发，目前只支持中文版本、BSC链查询 
        - /bee_check <代币合约地址>
        """
    )
    """Send a message when the command /help is issued."""
    update.message.reply_text(HELP_TEXT)


def auto_check_token(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    address = getAddress(update.message.text)
    if address == "":
        return
    tokenInfo = getTokenInfo(address)
    reply_message = buildMessage(tokenInfo['result'][address.lower()])
    update.message.reply_markdown(reply_message)


def check(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    address = getAddress(update.message.text)
    if address == "":
        return
    tokenInfo = getTokenInfo(address)
    reply_message = buildMessage(tokenInfo['result'][address.lower()])
    update.message.reply_markdown( reply_message)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=BOTAPIKEY, request_kwargs={'proxy_url': 'http://192.168.1.34:1080/'})

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("bee_check", auto_check_token))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_check_token))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()