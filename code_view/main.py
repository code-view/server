from asyncio import get_event_loop
from aiohttp import web
from .db import redis
from .router import router

app = web.Application(router=router)
loop = get_event_loop()
loop.run_until_complete(redis.init())

if __name__ == '__main__':
    web.run_app(app)
