from asyncio import get_event_loop
from logging.config import dictConfig
from aiohttp import web
from .db import redis
from .router import router
from . import settings

dictConfig(settings.LOGGING)
app = web.Application(router=router)
loop = get_event_loop()
loop.run_until_complete(redis.init())

if __name__ == '__main__':
    web.run_app(app)
