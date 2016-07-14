from aiohttp import web
from .handlers import create_session, get_session, update_session, subscribe

router = web.UrlDispatcher()
router.add_route('POST', '/api/session/', create_session)
router.add_route('PUT', '/api/session/{id}/', update_session)
router.add_route('GET', '/api/session/{id}/', get_session)
router.add_route('GET', '/channel/session/{id}/', subscribe)
