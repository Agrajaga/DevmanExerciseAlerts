import os

import requests
import telegram
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    devman_token = os.getenv("DEVMAN_API_TOKEN")
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_token)

    headers = {
        "Authorization": devman_token,
    }
    timeout = 120
    params = {}

    while True:
        try:
            response = requests.get(
                "https://dvmn.org/api/long_polling/",
                headers=headers,
                timeout=timeout,
                params=params)
            response.raise_for_status()
            user_reviews = response.json()

            params = {}
            if user_reviews["status"] == "timeout":
                params = {
                    "timestamp": user_reviews["timestamp_to_request"],
                }
            if user_reviews["status"] == "found":
                for attempt in user_reviews["new_attempts"]:
                    work_status = "Преподавателю все понравилось, можно приступать к следующему уроку!"
                    if attempt["is_negative"]:
                        work_status = "К сожалению в работе нашлись ошибки\."
                    work_desc = f'["{attempt["lesson_title"]}"]({attempt["lesson_url"]})'
                    message = f'Преподаватель проверил работу {work_desc}\. {work_status}'
                    bot.send_message(
                        chat_id=tg_chat_id,
                        text=message,
                        parse_mode=telegram.ParseMode.MARKDOWN_V2,
                        disable_web_page_preview=True,
                    )
        except requests.exceptions.ReadTimeout:
            print("No answer from server.")
        except requests.exceptions.ConnectionError:
            print("Connection error. Reconnecting...")
