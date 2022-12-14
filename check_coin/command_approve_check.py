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
"ð[BEECapital](https://beecapital.org/) `å¼åç»´æ¤ï¼æ¬¢è¿ä½¿ç¨ï¼`\n\
{} *å°åææä¿¡æ¯æ¥è¯¢:*\n\
{}\n\
"

    message = \
"\n{}({})\n\
è¢«ææåçº¦ï¼{}\n\
è¢«ææTokenï¼{}\n\
æææ¥æï¼{}\n\
æææ°éï¼{}\n\
é£é©ç³»æ°ï¼{}\n\
"

#     end_message = \
# ""
    address_simple = "0x..." + address[-6:]

    approve_tokens = input["result"]
    for approve_token in approve_tokens:
        #è¢«ææToken
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
                approved_amount = "æ é"
            approved_time = approve['approved_time']
            approved_time_fromat = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(approved_time)) + "(UTC)"
            doubt_list = approve['address_info']['doubt_list']
            trust_list = approve['address_info']['trust_list']
            risk = ""
            if doubt_list == 1:
                risk = "â ï¸é«"
            if trust_list == 1:
                risk = "ð¢ä½"
            if doubt_list == 0 and trust_list == 0:
                risk = "ð ä¸­"


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
                                InlineKeyboardButton('æ¥çæ­¤ä»£å¸æ´å¤ä¿¡æ¯', \
                                                    url = 'https://t.me/bee_check_details')]]))


handler = CommandHandler("approve_check", approve_check)
