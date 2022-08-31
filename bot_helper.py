import telegram  #pip install python-telegram-bot --upgrade


class BotHelper:
    def __init__(self, apikey):
        self.bot = telegram.Bot(token=apikey)

    def sendMessage(self, chat_id, text):
        self.bot.send_message(chat_id='@XXXXXX', text="新消息")

    def getMessage(self):




