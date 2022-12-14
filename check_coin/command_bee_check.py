# -*- coding: UTF-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import json
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



def getTokenInfo(token, apikey = GOAPIKEY, apisecrect = GOAPISECRECT):
        # params = {'api-key': apikey,
        #    'api-secrect:': apisecrect}
        # params["contract_addresses"] = token
        # result = httpx.get('https://api.gopluslabs.io/api/v1/token_security/56', params = params)
        # return json.loads(result.text)

        with open("../example/token.json", 'r') as f:
            temp = json.loads(f.read())
        return temp

def buildMessage(address, input):
    message = \
"ð[BEECapital](https://beecapital.org/) `å¼åç»´æ¤ï¼æ¬¢è¿ä½¿ç¨ï¼`\n\
*\n{}ï¼{}ï¼*\n\
1ï¸â£ *ä»£å¸ä¿¡æ¯*\n\
åçº¦ï¼[{}]({})\n\
åè¡æ»éï¼{}\n\
æµéæ»éï¼{}\n\
\n2ï¸â£ *äº¤æç¶æ*\n\
è½å¦ååºï¼{}\n\
ä¹°å¥ï¼{}%     ååºï¼{}%\n\
\n3ï¸â£ *ä»£ç ä¿¡æ¯*\n\
æ¯å¦å¼æºï¼{}\n\
åçº¦æææï¼{}\n\
éèæéï¼{}\n\
è°èç¨çï¼{}\n\
ä½é¢ä¿®æ¹ï¼{}\n\
æåäº¤æï¼{}\n\
\n4ï¸â£ *ç¸å³æ°æ®*\n\
æä»äººæ°ï¼{}\n\
\n`ä»¥ä¸æ°æ®ä»ä¾åèï¼ä¸ä½ä¸ºæèµå»ºè®®ï¼`\
"

    message2 = \
"ð[BEECapital](https://beecapital.org/) `å¼åç»´æ¤ï¼æ¬¢è¿ä½¿ç¨ï¼`\n\
*\n{}ï¼{}ï¼*\n\
1ï¸â£ *ä»£å¸ä¿¡æ¯*\n\
é¾/IDï¼BSC/56\n\
åçº¦ï¼[{}]({})\n\
åå»ºèï¼[{}]({})\n\
åè¡æ»éï¼{}\n\
æµéæ»éï¼{}\n\
\n2ï¸â£ *äº¤æç¶æ*\n\
ä¸çº¿çDEXï¼{}\n\
è½å¦ååºï¼{}\n\
ä¹°å¥ï¼{}%     ååºï¼{}%\n\
\n3ï¸â£ *ä»£ç ä¿¡æ¯*\n\
æ¯å¦å¼æºï¼{}\n\
åçº¦æææï¼{}\n\
ä»£çåçº¦ï¼{}\n\
éèæéï¼{}\n\
è°èç¨çï¼{}\n\
ä½é¢ä¿®æ¹ï¼{}\n\
æåäº¤æï¼{}\n\
ç½ååï¼{}\n\
é»ååï¼{}\n\
\n4ï¸â£ *ç¸å³æ°æ®*\n\
æä»äººæ°ï¼{}\n\
æµå¨æ§æ± ï¼å·²éå®{}\n\
éä»æ°æ®ï¼{}\n\
\n`ä»¥ä¸æ°æ®ä»ä¾åèï¼ä¸ä½ä¸ºæèµå»ºè®®ï¼`\
"

    # åç§°
    name = input['token_name']
    symbol = input['token_symbol']

    # åçº¦
    contract = "0x...." + address[-6:]
    url = "https://bscscan.com/token/" + address.lower() + "#tokenInfo"

    # ä¹°å¥
    buy_tax = "æªç¥"
    if "buy_tax" in input:
        buy_tax = '%.2f'%(float(input['buy_tax']) * 100)

    # ååº
    sell_tax = "æªç¥"
    if "sell_tax" in input:
        sell_tax = '%.2f'%(float(input['sell_tax']) * 100)
        if float(sell_tax) >= 100:
            sell_tax = "âï¸100"
    

    # ææäººæ°
    holder = input['holder_count']

    # æ»åè¡é
    supply = '%.2f'%(float(input['total_supply']))

    #è½¬è´¦å¼å³/è°èç¨ç
    transfer_pausable = "æªç¥"
    if "transfer_pausable" in input:
        transfer_pausable = input["transfer_pausable"]
        if transfer_pausable == "0" :
            transfer_pausable = "ð¢ä¸è½"
        else:
            transfer_pausable = "â ï¸å¯ä»¥"

    #æ»ç¹æ´æ¹
    slippage_modifiable = "æªç¥"
    if "slippage_modifiable" in input:
        slippage_modifiable = input["slippage_modifiable"]
        if slippage_modifiable == "0" :
            slippage_modifiable = "ð¢ä¸è½"
        else:
            slippage_modifiable = "â ï¸å¯ä»¥"

    #ææè
    owner = input["owner_address"]
    if owner == "0x0000000000000000000000000000000000000000" or owner.lower() == "0x000000000000000000000000000000000000dead":
        owner = "ð¢å·²æ¾å¼"
    else:
        owner = "â ï¸æªæ¾å¼"


    #éèæé
    hidden_owner = "æªç¥"
    if "hidden_owner" in input:
        hidden_owner = input["hidden_owner"]
        if hidden_owner == "0" :
            hidden_owner = "ð¢ä¸è½"
        else:
            hidden_owner = "â ï¸å¯ä»¥"


    #å¤é¨è°ç¨
    external_call = "æªç¥"
    if "external_call" in input:
        external_call = input["external_call"]
        if external_call == "0":
            external_call = "ð¢æ "
        else:
            external_call = "â ï¸æ"

    #åè®¸è´­ä¹°
    cannot_buy = "æªç¥"
    if "cannot_buy" in input:
        cannot_buy = input["cannot_buy"]
        if cannot_buy == "0":
            cannot_buy = "ð¢å¯"
        else:
            cannot_buy = "â ï¸å¦"

    #åè®¸åºå®
    cannot_sell_all = "æªç¥"
    if "cannot_sell_all" in input:
        cannot_sell_all = input["cannot_sell_all"]
        if cannot_sell_all == "0":
            cannot_sell_all = "ð¢"
        else:
            cannot_sell_all = "ð´"
    
    #ä»£çåçº¦
    is_proxy = "æªç¥"
    if "is_proxy" in input:
        is_proxy =  input["is_proxy"]
        if is_proxy == "0":
            is_proxy = "ð¢å¦"
        else:
            is_proxy = "â ï¸æ¯"

    #èç¾
    is_honeypot = "æªç¥"
    if "is_honeypot" in input:
        is_honeypot = input["is_honeypot"]
        if is_honeypot == "0":
            is_honeypot = "ð¢å¦"
        else:
            is_honeypot = "âï¸æ¯"

    #å¯å¢å
    is_mintable = "æªç¥"
    if "is_mintable" in input:
        is_mintable = input["is_mintable"]
        if is_mintable == "0":
            is_mintable = "ð¢ä¸è½"
        else:
            is_mintable = "â ï¸å¯ä»¥"

    #ç½åå
    is_whitelisted = "æªç¥"
    if "is_whitelisted" in input:
        is_whitelisted = input["is_whitelisted"]
        if is_whitelisted == "0":
            is_whitelisted = "ð¢æ "
        else:
            is_whitelisted = "â ï¸æ"

    #é»åå
    is_blacklisted = "æªç¥"
    if "is_blacklisted" in input:
        is_blacklisted = input["is_blacklisted"]
        if is_blacklisted == "0":
            is_blacklisted = "ð¢æ "
        else:
            is_blacklisted = "â ï¸æ"

    #æå¤§æ± å­
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
    



    #ä»£å¸æä»
    holders = input["holders"]
    destroy = "æ "
    pool_amount = "æ "
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
                lock  = lock + "\n" + str(index) + "ãéå®æ°éï¼" + '%.2f'%float(locked_detail["amount"]) \
                + "\n       ç»ææ¶é´ï¼" + locked_detail["end_time"]
                not_flow_amount = not_flow_amount + float(locked_detail["amount"])
                index = index + 1

        # if info["is_contract"] == 1 and info["address"].lower() == pair:
        #     t = float(info["balance"]) / float(supply) * 100
        #     pool_amount = '%.2f'%t + "%"\
        #         + " (" + info["tag"] + ")"




    #æ± å­æä»
    lp_total_supply = input["lp_total_supply"]
    lp_holders = input["lp_holders"]
    destroy = "æ "
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

    #æµéæ»é
    flow_amount = float(supply) - not_flow_amount
    flow_amount = '%.2f'%flow_amount

    is_open_source = input["is_open_source"]
    if is_open_source == "0":
        is_open_source = "ð´"
    else:
        is_open_source = "ð¢"

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


def auto_check_token(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    address = utils.getAddress(update.message.text)
    if address == "":
        return
    tokenInfo = getTokenInfo(address)
    user = update.effective_user
    reply_message, reply_message2 = buildMessage(address, tokenInfo['result'][address.lower()])
    update.message.reply_markdown(reply_message, disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup([[ \
                                  InlineKeyboardButton('æ¥çæ­¤ä»£å¸æ´å¤ä¿¡æ¯', \
                                                       url = 'https://t.me/bee_check_details')]]))
    reply_message2 = "@" + user.full_name + "\n" + reply_message2
    context.bot.send_message(chat_id = CHANNEL, text = reply_message2, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def check(update: Update, context: CallbackContext) -> None:
    address = utils.getAddress(update.message.text)
    if address == "":
        return
    tokenInfo = getTokenInfo(address)
    reply_message, reply_message2 = buildMessage(address, tokenInfo['result'][address.lower()])
    update.message.reply_markdown(reply_message, disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup([[ \
                                  InlineKeyboardButton('æ¥çæ­¤ä»£å¸æ´å¤ä¿¡æ¯', \
                                                       url = 'https://t.me/bee_check_details')]]))
    context.bot.send_message(chat_id = CHANNEL, text = reply_message2, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

handler = CommandHandler("bee_check", auto_check_token)