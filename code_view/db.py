import abc
from typing import Generic, AsyncIterator, T

from asyncio_redis import Connection, RedisProtocol
from .settings import REDIS_OPTIONS


class _RedisProxy:
    """Proxy for late initialization of redis connection."""

    def __init__(self):
        self._connection = None

    @staticmethod
    async def create() -> Connection:
        """Create new redis connection."""
        return await Connection.create(**REDIS_OPTIONS)

    async def init(self):
        self._connection = await self.create()

    def __getattr__(self, item):
        return getattr(self._connection, item)


redis = _RedisProxy()  # type: RedisProtocol


class Subscription(Generic[T]):
    """Async iterator for receiving channel messages."""

    def __init__(self, keys):
        self._keys = keys
        self._subscription = None

    @abc.abstractclassmethod
    def _map(self, content: str) -> T:
        """Transform value from redis to python."""

    async def _subscribe(self):
        """Subscribe to redis PUB/SUB."""
        conn = await redis.create()
        self._subscription = await conn.start_subscribe()
        await self._subscription.subscribe(self._keys)

    async def __aiter__(self) -> AsyncIterator[T]:
        if self._subscription is None:
            await self._subscribe()
        return self

    async def __anext__(self) -> T:
        reply = await self._subscription.next_published()
        return self._map(reply.value)
