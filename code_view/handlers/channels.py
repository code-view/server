import json
from aiohttp import web
from ..models.session import Session


async def subscribe_to_session(request: web.Request) -> web.WebSocketResponse:
    """Subscribe to session updates.

    Changed session will be pushed to client via web socket.

    """
    session = await Session.objects.get(request.match_info['id'])
    if session is None:
        return web.HTTPNotFound()

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for update in session.subscribe():
        ws.send_str(json.dumps(update.as_safe_dict))

    return ws
