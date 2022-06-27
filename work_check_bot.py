import logging
import os
from time import sleep

import requests
import telegram
from dotenv import load_dotenv

logger = logging.getLogger("tg_devman_alert")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot: telegram.Bot, chat_id: int) -> None:
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    load_dotenv()
    devman_token = os.getenv("DEVMAN_API_TOKEN")
    tg_token = os.getenv("TG_BOT_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")

    bot = telegram.Bot(token=tg_token)

    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(message)s"
    )
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(tg_bot=bot, chat_id=tg_chat_id))
    logger.warning("Start logging")

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

            if user_reviews["status"] == "timeout":
                params = {
                    "timestamp": user_reviews["timestamp_to_request"],
                }
            if user_reviews["status"] == "found":
                params = {
                    "timestamp": user_reviews["last_attempt_timestamp"],
                }
                for attempt in user_reviews["new_attempts"]:
                    work_status = "Преподавателю все понравилось,\
 можно приступать к следующему уроку!"
                    if attempt["is_negative"]:
                        work_status = "К сожалению в работе нашлись ошибки."
                    work_desc = f'<a href="{attempt["lesson_url"]}">\
"{attempt["lesson_title"]}"</a>'
                    message = f"Преподаватель проверил работу {work_desc}.\n\
{work_status}"
                    bot.send_message(
                        chat_id=tg_chat_id,
                        text=message,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
        except requests.exceptions.ReadTimeout:
            logger.warning("No answer from server.")
        except requests.exceptions.ConnectionError:
            sleep(300)
            logger.warning("Connection error. Reconnecting...")
        except Exception:
            logger.exception(msg="Бот упал с ошибкой")
