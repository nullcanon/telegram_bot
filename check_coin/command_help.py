# -*- coding: UTF-8 -*-

from telegram import Update,  InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext


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

handler = CommandHandler("help", help_command)