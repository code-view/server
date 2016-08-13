from aiohttp import web
from ..models.session import Session


async def create_session(_: web.Request) -> web.Response:
    """Create new session."""
    session = await Session.objects.create()
    return web.json_response(session.as_dict, status=201)


async def update_session(request: web.Request) -> web.Response:
    """Update existing session."""
    data = await request.json()
    if data['id'] != request.match_info['id']:
        return web.HTTPBadRequest()

    session = await Session.objects.get(request.match_info['id'])
    if session is None:
        return web.HTTPNotFound()

    if session.secureToken != data['secureToken']:
        return web.HTTPForbidden()

    session = await session.update(**data)
    return web.json_response(session.as_dict)


async def get_session(request: web.Request) -> web.Response:
    """Get existing session."""
    session = await Session.objects.get(request.match_info['id'])
    if session is None:
        return web.HTTPNotFound()
    else:
        return web.json_response(session.as_safe_dict)
