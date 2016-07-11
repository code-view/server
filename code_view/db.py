from typing import NamedTuple, Optional
from uuid import uuid4
import json
from asyncio_redis import Connection, RedisProtocol
from .settings import REDIS_OPTIONS


class _RedisProxy:
    def __init__(self):
        self._connection = None

    async def init(self):
        self._connection = await Connection.create(**REDIS_OPTIONS)

    def __getattr__(self, item):
        return getattr(self._connection, item)


redis = _RedisProxy()  # type: Optional[RedisProtocol]

Session = NamedTuple('Session', [('id', str),
                                 ('fileName', Optional[str]),
                                 ('text', Optional[str]),
                                 ('selectionStartLine', Optional[int]),
                                 ('selectionStartColumn', Optional[int]),
                                 ('selectionEndLine', Optional[int]),
                                 ('selectionEndColumn', Optional[int])])


def key(session_id: str) -> str:
    return 'session:{}'.format(session_id)


async def save(session: Session):
    serialized = json.dumps(session._asdict())
    entry_key = key(session.id)
    await redis.set(entry_key, serialized)


async def create() -> Session:
    session = Session(id=uuid4().hex,
                      fileName=None,
                      text=None,
                      selectionStartLine=None,
                      selectionStartColumn=None,
                      selectionEndLine=None,
                      selectionEndColumn=None)
    await save(session)
    return session


async def get(id: str) -> Session:
    serialized = await redis.get(key(id))
    if not serialized:
        return

    data = json.loads(serialized)
    return Session(**data)
