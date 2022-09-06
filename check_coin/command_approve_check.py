# -*- coding: UTF-8 -*-

from telegram.ext import CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import json
import time
from datetime import datetime
import utils

def loadConfig():
    with open("./config.json","r") as f:
        load_dict = json.load(f)
    return load_dict

config = loadConfig()
GOAPIKEY = config['go_plus_api_key']
GOAPISECRECT = config['go_plus_api_secrect']
BOTAPIKEY =  config['bot_api_key']
CHANNEL = config['token_check_channel_id']


def buildMessage(address, input):
    base_message = \
"🔆[BEECapital](https://beecapital.org/) `开发维护，欢迎使用！`\n\
{} *地址授权信息查询:*\n\
{}\n\
"

    message = \
"\n{}({})\n\
被授权合约：{}\n\
被授权Token：{}\n\
授权日期：{}\n\
授权数量：{}\n\
风险系数：{}\n\
"

#     end_message = \
# ""
    address_simple = "0x..." + address[-6:]

    approve_tokens = input["result"]
    for approve_token in approve_tokens:
        #被授权Token
        token = approve_token['token_address']

        token_name = approve_token['token_name']
        token_symbol = approve_token['token_symbol']
        approved_list = approve_token['approved_list']
        times = 0
        for approve in approved_list:
            times = times + 1
            if times >= 2:
                break
            approved_contract = approve['approved_contract']
            approved_amount = approve['approved_amount']
            if approved_amount == "Unlimited":
                approved_amount = "无限"
            approved_time = approve['approved_time']
            approved_time_fromat = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(approved_time)) + "(UTC)"
            doubt_list = approve['address_info']['doubt_list']
            trust_list = approve['address_info']['trust_list']
            risk = ""
            if doubt_list == 1:
                risk = "⚠️高"
            if trust_list == 1:
                risk = "🟢低"
            if doubt_list == 0 and trust_list == 0:
                risk = "🟠中"


            message = message + message.format(token_name, token_symbol, approved_contract, token, approved_time_fromat,
                approved_amount, risk)


    message_in_detail = base_message.format(address_simple, message)
    return message_in_detail





def getApproveInfo(account, apikey = GOAPIKEY, apisecrect = GOAPISECRECT):
        # params = {'api-key': apikey,
        #    'api-secrect:': apisecrect}
        # params["contract_addresses"] = token
        # result = httpx.get('https://api.gopluslabs.io/api/v1/token_security/56', params = params)
        # return json.loads(result.text)

        with open("../example/approve.json", 'r') as f:
            temp = json.loads(f.read())
        return temp


def approve_check(update: Update, context: CallbackContext) -> None:
    address = utils.getAddress(update.message.text)
    approve_info = getApproveInfo(address)
    message = buildMessage(address, approve_info)
    update.message.reply_markdown(message, disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup([[ \
                                InlineKeyboardButton('查看此代币更多信息', \
                                                    url = 'https://t.me/bee_check_details')]]))


handler = CommandHandler("approve_check", approve_check)
