import asyncio
import os

import telegram
from dotenv import load_dotenv


async def main(token):
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text='Hi John!', chat_id=1724291408)

if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    asyncio.run(main(tg_token))
