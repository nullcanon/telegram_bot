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
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
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
CHANNEL = config['token_check_channel_id']

def getTokenInfo(token, apikey = GOAPIKEY, apisecrect = GOAPISECRECT):
        # params = {'api-key': apikey,
        #    'api-secrect:': apisecrect}
        # params["contract_addresses"] = token
        # result = httpx.get('https://api.gopluslabs.io/api/v1/token_security/56', params = params)
        # return json.loads(result.text)

        with open("./example.json", 'r') as f:
            temp = json.loads(f.read())
        return temp

def getAddress(text):
    index = text.find('0')
    if index == -1:
        return ""
    address = text[index:]
    if not Web3.isAddress(address):
        return ""
    return address

    
def buildMessage(address, input):
    message = \
"🔆[BEECapital](https://beecapital.org/) `开发维护，欢迎使用！`\n\
*{}（{}）*\n\
1️⃣ *代币信息*\n\
合约：[{}]({})\n\
发行总量：{}\n\
流通总量：{}\n\
\n2️⃣ *交易状态*\n\
能否卖出：{}\n\
买入：{}%     卖出：{}%\n\
\n3️⃣ *代码信息*\n\
是否开源：{}\n\
合约所有权：{}\n\
隐藏权限：{}\n\
调节税率：{}\n\
余额修改：{}\n\
暂停交易：{}\n\
\n4️⃣ *相关数据*\n\
持仓人数：{}\n\
\n`以上数据仅供参考，不作为投资建议！`\
"

    message2 = \
"🔆[BEECapital](https://beecapital.org/) `开发维护，欢迎使用！`\n\
*{}（{}）*\n\
1️⃣ *代币信息*\n\
链/ID：BSC/56\n\
合约：[{}]({})\n\
创建者：[{}]({})\n\
发行总量：{}\n\
流通总量：{}\n\
\n2️⃣ *交易状态*\n\
上线的DEX：{}\n\
能否卖出：{}\n\
买入：{}%     卖出：{}%\n\
\n3️⃣ *代码信息*\n\
是否开源：{}\n\
合约所有权：{}\n\
代理合约：{}\n\
隐藏权限：{}\n\
调节税率：{}\n\
余额修改：{}\n\
暂停交易：{}\n\
白名单：{}\n\
黑名单：{}\n\
\n4️⃣ *相关数据*\n\
持仓人数：{}\n\
流动性池：已锁定{}\n\
锁仓数据：{}\n\
\n`以上数据仅供参考，不作为投资建议！`\
"

    # 名称
    name = input['token_name']
    symbol = input['token_symbol']

    # 合约
    contract = "0x...." + address[-6:]
    url = "https://bscscan.com/token/" + address.lower() + "#tokenInfo"

    # 买入
    buy_tax = "未知"
    if "buy_tax" in input:
        buy_tax = '%.2f'%(float(input['buy_tax']) * 100)

    # 卖出
    sell_tax = "未知"
    if "sell_tax" in input:
        sell_tax = '%.2f'%(float(input['sell_tax']) * 100)
        if float(sell_tax) >= 100:
            sell_tax = "❗️100"
    

    # 持有人数
    holder = input['holder_count']

    # 总发行量
    supply = '%.2f'%(float(input['total_supply']))

    #转账开关/调节税率
    transfer_pausable = "未知"
    if "transfer_pausable" in input:
        transfer_pausable = input["transfer_pausable"]
        if transfer_pausable == "0" :
            transfer_pausable = "🟢不能"
        else:
            transfer_pausable = "⚠️可以"

    #滑点更改
    slippage_modifiable = "未知"
    if "slippage_modifiable" in input:
        slippage_modifiable = input["slippage_modifiable"]
        if slippage_modifiable == "0" :
            slippage_modifiable = "🟢不能"
        else:
            slippage_modifiable = "⚠️可以"

    #所有者
    owner = input["owner_address"]
    if owner == "0x0000000000000000000000000000000000000000" or owner.lower() == "0x000000000000000000000000000000000000dead":
        owner = "🟢已放弃"
    else:
        owner = "⚠️未放弃"


    #隐藏权限
    hidden_owner = "未知"
    if "hidden_owner" in input:
        hidden_owner = input["hidden_owner"]
        if hidden_owner == "0" :
            hidden_owner = "🟢不能"
        else:
            hidden_owner = "⚠️可以"


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
            cannot_sell_all = "🟢"
        else:
            cannot_sell_all = "🔴"
    
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
            is_mintable = "🟢不能"
        else:
            is_mintable = "⚠️可以"

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
    max_dex = ""
    up_dex = {}
    for pool in dexs:
        up_dex[pool["name"]] = 1
    for key in up_dex.keys():
        if max_dex == "":
            max_dex = key
        else:
            max_dex = max_dex + "/" + key
    



    #代币持仓
    holders = input["holders"]
    destroy = "无"
    pool_amount = "无"
    lock = ""
    not_flow_amount = 0
    for info in holders:
        if info["is_locked"] == 1 and info["address"] == "0x000000000000000000000000000000000000dead":
            t = float(info["balance"]) / float(supply) * 100
            destroy = '%.2f'%t + "%"
            not_flow_amount = not_flow_amount + float(info["balance"])
            
        if info["is_locked"] == 1 and "locked_detail" in info:
            lock = ""
            index = 1
            for locked_detail in info["locked_detail"]:
                lock  = lock + "\n" + str(index) + "、锁定数量：" + '%.2f'%float(locked_detail["amount"]) \
                + "\n       结束时间：" + locked_detail["end_time"]
                not_flow_amount = not_flow_amount + float(locked_detail["amount"])
                index = index + 1

        # if info["is_contract"] == 1 and info["address"].lower() == pair:
        #     t = float(info["balance"]) / float(supply) * 100
        #     pool_amount = '%.2f'%t + "%"\
        #         + " (" + info["tag"] + ")"




    #池子持仓
    lp_total_supply = input["lp_total_supply"]
    lp_holders = input["lp_holders"]
    destroy = "无"
    locked_amount = 0
    for info in lp_holders:
        if info["is_locked"] == 1 and info["address"] == "0x000000000000000000000000000000000000dead":
            t = float(info["balance"]) / float(lp_total_supply) * 100
            destroy = '%.2f'%t + "%"

        if info["is_locked"] == 1 and "locked_detail" in info:
            for locked_detail in info["locked_detail"]:
                locked_amount = locked_amount + float(locked_detail["amount"])
    t = locked_amount/float(lp_total_supply) * 100
    locked_amount = '%.2f'%t + "%"


    # lp_lock = lp_lock.format(destroy, lock)

    #流通总量
    flow_amount = float(supply) - not_flow_amount
    flow_amount = '%.2f'%flow_amount

    is_open_source = input["is_open_source"]
    if is_open_source == "0":
        is_open_source = "🔴"
    else:
        is_open_source = "🟢"

    creator_address = input["creator_address"]
    creator_address_simple = "0x..." + creator_address[-6:]
    creator_url = "https://bscscan.com/address/" + creator_address_simple.lower()

    message_in_simple = message.format(name, symbol, contract, url, supply, flow_amount, cannot_sell_all, buy_tax, 
        sell_tax, is_open_source, owner, hidden_owner,
        slippage_modifiable, is_mintable, transfer_pausable, holder)

    message_in_detail = message2.format(name, symbol, contract, url,creator_address_simple, creator_url, supply, flow_amount, max_dex, 
        cannot_sell_all, buy_tax, sell_tax, is_open_source, owner, is_proxy, hidden_owner,
        slippage_modifiable, is_mintable, transfer_pausable, is_whitelisted, is_blacklisted,
        holder, locked_amount, lock)
    return message_in_simple, message_in_detail




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
        - /bee_check  <代币合约地址>
        - /approve_check  <钱包地址>
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
    reply_message, reply_message2 = buildMessage(address, tokenInfo['result'][address.lower()])
    update.message.reply_markdown(reply_message, disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup([[ \
                                  InlineKeyboardButton('查看此代币更多信息', \
                                                       url = 'https://t.me/bee_check_details')]]))
    context.bot.send_message(chat_id = CHANNEL, text = reply_message2, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def check(update: Update, context: CallbackContext) -> None:
    address = getAddress(update.message.text)
    if address == "":
        return
    tokenInfo = getTokenInfo(address)
    reply_message, reply_message2 = buildMessage(address, tokenInfo['result'][address.lower()])
    update.message.reply_markdown(reply_message, disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup([[ \
                                  InlineKeyboardButton('查看此代币更多信息', \
                                                       url = 'https://t.me/bee_check_details')]]))
    context.bot.send_message(chat_id = CHANNEL, text = reply_message2, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def approve_check() -> None:
    pass

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
    dispatcher.add_handler(CommandHandler("approve_check", approve_check))

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