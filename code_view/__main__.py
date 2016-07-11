from asyncio import get_event_loop
from aiohttp import web
from .db import redis
from .router import router
from .middlewares import debug

if __name__ == '__main__':
    app = web.Application(router=router,
                          middlewares=[debug])
    loop = get_event_loop()
    loop.run_until_complete(redis.init())
    web.run_app(app)
