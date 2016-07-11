import pytest
from asyncio_redis import Connection

from code_view.db import redis
from code_view.settings import TEST_REDIS_OPTIONS


@pytest.fixture(autouse=True)
def redis_db(request, event_loop):
    async def _clear_db():
        redis = await init_db()
        await redis.flushdb()

    @request.addfinalizer
    def _finalizer():
        event_loop.run_until_complete(_clear_db())

    async def init_db():
        redis._connection = await Connection.create(**TEST_REDIS_OPTIONS)
        return redis._connection

    event_loop.run_until_complete(init_db())
