from os import getenv
import requests

secret = getenv("SECRET")
mq_url = getenv("MQ")

class Secret:
    def __init__(self):
        res = requests.get(secret).json()
        self.api_id = res['key'].get('api_id')
        self.api_hash = res['key'].get('api_hash')
        self.bot_token = res['bot'].get('nw_tg')
        
values = Secret()
api_id = values.api_id
api_hash = values.api_hash
bot_token = values.bot_token