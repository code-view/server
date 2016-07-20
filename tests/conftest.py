from asyncio import set_event_loop

import pytest
from aiohttp import web

from code_view.db import redis
from code_view.settings import TEST_REDIS_OPTIONS
from code_view.router import router

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.yield_fixture(autouse=True)
def redis_db(loop, monkeypatch):
    """Use test redis config."""
    monkeypatch.setattr('code_view.db.REDIS_OPTIONS', TEST_REDIS_OPTIONS)
    loop.run_until_complete(redis.init())
    yield
    loop.run_until_complete(redis.flushdb())


@pytest.fixture(autouse=True)
def global_loop(loop):
    set_event_loop(loop)


def _create_app(loop):
    return web.Application(router=router, loop=loop)


@pytest.fixture
def client(loop, test_client):
    return loop.run_until_complete(test_client(_create_app))
