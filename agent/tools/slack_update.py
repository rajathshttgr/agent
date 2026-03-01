import requests
import os
from dotenv import load_dotenv

load_dotenv()

slack_url = os.getenv("SLACK_BOT_URL")


def send_slack_message(message: str):
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(slack_url, json=payload, headers=headers)
    if response.status_code != 200:
        print(
            f"Failed to send message to Slack: {response.status_code} - {response.text}"
        )
        return False
    print("Message sent to Slack successfully")
    return True


if __name__ == "__main__":
    send_slack_message("Hello from the Slack bot!")
