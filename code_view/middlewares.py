from aiohttp import web

from . import settings


async def debug(app, handler):
    async def middleware_handler(request: web.Request) -> web.Response:
        if settings.DEBUG:
            try:
                response = await handler(request)
                print(request.method, request.path, '->',
                      response.status, ':', response.reason)
                return response
            except Exception as e:
                print(request.method, request.path)
                print(await request.json())
                raise e

        return await handler(request)

    return middleware_handler
