import os

from dotenv import load_dotenv
import telegram


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_token)
    bot.send_message(chat_id=tg_chat_id, text="Привет, Михаил!")
