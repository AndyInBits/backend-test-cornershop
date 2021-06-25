import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send_message_slack(menu_url):
    slack_token = os.environ["SLACK_API_TOKEN"]
    channel = os.environ["SLACK_CHANNEL_ID"]
    client = WebClient(token=slack_token)
    site_url = os.environ["FRONT_SITE_URL"]
    message = f""" ¡Hola! \n Comparto con ustedes el menú de hoy :) \n Menu : {site_url}{menu_url} """

    try:
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        # str like 'invalid_auth', 'channel_not_found'
        assert e.response["error"]
