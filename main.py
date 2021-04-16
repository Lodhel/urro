import aiohttp_cors
from aiohttp import web

import asyncio

from views import routes
from models import BaseLogic


class Main:

    def _run(self):
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
        app.router.add_routes(routes)
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
        })

        for route in list(app.router.routes()):
            cors.add(route)

        web.run_app(app)

    async def task_is_calc(self):
        while True:
            await BaseLogic().check()  # TODO here your logic, and this object from models.py
            await asyncio.sleep(86400)
