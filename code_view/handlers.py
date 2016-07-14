import json

from aiohttp import web
from . import db


async def create_session(request: web.Request) -> web.Response:
    session = await db.create()
    return web.json_response(session._asdict(), status=201)


async def update_session(request: web.Request) -> web.Response:
    data = await request.json()
    if data['id'] != request.match_info['id']:
        return web.HTTPBadRequest()

    session = db.Session(**data)
    await db.save(session)
    return web.json_response(session._asdict())


async def get_session(request: web.Request) -> web.Response:
    session_id = request.match_info['id']
    session = await db.get(session_id)
    if session is None:
        return web.HTTPNotFound()
    else:
        return web.json_response(session._asdict())


async def subscribe(request: web.Request) -> web.WebSocketResponse:
    session_id = request.match_info['id']
    session = await db.get(session_id)
    if session is None:
        return web.HTTPNotFound()

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    subscription = await db.subscribe(session)

    async for session in subscription:
        ws.send_str(json.dumps(session._asdict()))

    return ws
