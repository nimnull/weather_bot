import asyncio
import logging
import sys

from http import HTTPStatus
from urllib.parse import urljoin

import aiohttp
import datetime

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)
BOT_TOKEN = "change me"



class TelegramBot:
    BASE_URI = "https://api.telegram.org/bot{token}/"

    def __init__(self, session, token):
        self.session = session
        self.token = token
        self.update_offset = 0

    def _get_uri(self, endpoint):
        return urljoin(self.BASE_URI.format(token=self.token), endpoint)

    async def _raise_for_status(self, resp):
        if resp.status == HTTPStatus.OK:
            rv = await resp.json()
            resp.release()
            return rv
        else:
            rv = await resp.text()
            resp.close()
            raise ValueError("Status: %s\n%s", resp.status, rv)

    def _raise_for_response(self, response):
        if response['ok']:
            return response['result']
        else:
            msg = "{error_code} | {description} ".format(**response)
            raise ValueError(msg)

    async def send_message(self, chat, sender=None):
        payload = {
            'chat_id': chat['id'],
            'text': 'confirmed at {}'.format(datetime.datetime.now().isoformat('T'))
        }
        resp = await self.session.post(self._get_uri('sendMessage'), data=payload)
        r_data = await self._raise_for_status(resp)
        try:
            result = self._raise_for_response(r_data)
            log.info("sent: %s", result)
        except ValueError as ex:
                log.error("Message send failed %s", ex)

    async def broadcast(self, message):
        pass

    async def get_updates(self):
        uri = self._get_uri('getUpdates')
        params = self.update_offset and {'offset': self.update_offset} or None
        resp = await self.session.get(uri, params=params)

        r_data = await self._raise_for_status(resp)
        try:
            result = self._raise_for_response(r_data)
            if len(result):
                await self.on_update(result)
        except ValueError as ex:
            log.error("Failed to retrieve updates: %s", ex)

    async def on_update(self, data):
        last_update = max(map(lambda r: r['update_id'], data))
        for update in data:
            message = update.get('message')
            if message:
                await self.on_message(message)
                log.info("received: %s", message)
        self.update_offset = last_update + 1

    async def on_message(self, message):
        await self.send_message(message['chat'], message.get('from'))
        entities = message.get('entities')


def init(loop, token):
    conn = aiohttp.TCPConnector(limit=5, conn_timeout=15,
                                use_dns_cache=True)
    session = aiohttp.ClientSession(connector=conn, loop=loop)
    bot = TelegramBot(session, token)

    return bot

