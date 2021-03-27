from aiohttp import web

import asyncio
import requests
from models import DebtorCard


class BaseMixin:
    async def check_passport(self, passport):
        params = {
            "token": "token",
            "num": passport
        }
        request = requests.post("https://www.passport-api.ru/api/1.0/", params=params)

    async def check_name(self, name):
        pass

    async def check_address(self, address):
        pass


class BaseLogic(BaseMixin):
    async def check_data(self):
        cards = await DebtorCard.query.where(DebtorCard.validation == False).gino.all()
        for card in cards:
            await self.check_passport(card.num_of_passport)
            await self.check_name(card.full_name)
            await self.check_address(card.address_debtor)


class Main:

    def _run(self):
        loop = asyncio.get_event_loop()
        app = web.Application(loop=loop)
        web.run_app(app)

    async def task_check_datacard(self):
        while True:
            await asyncio.sleep(86400)