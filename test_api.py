import os
from dotenv import load_dotenv
import requests
import pprint


if __name__ == "__main__":
    load_dotenv()
    devman_token = os.getenv("DEVMAN_API_TOKEN")

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
            answer = response.json()

            pprint.pprint(answer)
            params = {}
            if answer["status"] == "timeout":
                params = {
                    "timestamp": answer["timestamp_to_request"],
                }
        except requests.exceptions.ReadTimeout:
            print("Timeout")
        except requests.exceptions.ConnectionError:
            pass