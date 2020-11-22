import config_bot
import requests


def send_message_from_bot(text):
    for chat_id in config_bot.chat_id_list:
        req_message = f"https://api.telegram.org/bot{config_bot.token}/sendMessage?chat_id={chat_id}&text={text}"
        # print(req_message)
        res = requests.get(req_message)
