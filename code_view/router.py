from aiohttp import web
from .handlers.api import create_session, get_session, update_session
from .handlers.channels import subscribe_to_session

router = web.UrlDispatcher()
router.add_route('POST', '/api/session/', create_session)
router.add_route('PUT', '/api/session/{id}/', update_session)
router.add_route('GET', '/api/session/{id}/', get_session)
router.add_route('GET', '/channel/session/{id}/', subscribe_to_session)
