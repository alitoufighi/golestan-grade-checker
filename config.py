import os
import json
import platform
from exceptions import *
from pathlib import Path
from dotenv import load_dotenv


class GolestanGradeCheckerConfig:
    def __init__(self):
        try:
            self.term, self.tg_notif, self.login_url, self.refresh_rate, self.sms_notif = self._read_config()
        except InvalidJsonConfigFileException:
            exit(2)
        else:
            self.os = 'OSx' if platform.system() == 'Darwin' else 'Linux'
            self.username, self.password, self.tg_token, self.tg_chat_id, self.sms_api_key, self.phone_number = \
                self._read_env_config()

    def _read_env_config(self):
        load_dotenv(verbose=False)
        env_path = Path('./env') / '.env'
        load_dotenv(dotenv_path=str(env_path))

        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        tg_token = os.getenv("TOKEN")
        tg_chat_id = os.getenv("CHAT_ID")
        sms_api_key = os.getenv("SMS_KEY")
        phone_number = os.getenv("PHONE")
        return username, password, tg_token, tg_chat_id, sms_api_key, phone_number

    def _read_config(self):
        with open('config.json') as f:
            data = json.load(f)

        if 'term_no' not in data:
            raise InvalidJsonConfigFileException('term_no')
        if 'tele_notif' not in data:
            raise InvalidJsonConfigFileException('tele_notif')
        if 'golestan_login_url' not in data:
            raise InvalidJsonConfigFileException('golestan_login_url')
        if 'sms_notif' not in data:
            raise InvalidJsonConfigFileException('sms_notif')
        if 'refresh_rate' not in data:
            raise InvalidJsonConfigFileException('refresh_rate')

        return data['term_no'], data['tele_notif'], data['golestan_login_url'], data['refresh_rate'], data['sms_notif']
