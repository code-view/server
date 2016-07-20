import json
from typing import NamedTuple, Optional
from uuid import uuid4
from .. import db

# We use camel case here because most client's langs code styles
# prefer it (java, js).
_SessionEntity = NamedTuple('Session', [('id', str),
                                        ('fileName', Optional[str]),
                                        ('text', Optional[str]),
                                        ('selectionStartLine', Optional[int]),
                                        ('selectionStartColumn', Optional[int]),
                                        ('selectionEndLine', Optional[int]),
                                        ('selectionEndColumn', Optional[int])])

_get_key = 'session:{}'.format
_get_channel_key = 'channel:session:{}'.format


class SessionManager:
    async def create(self, *,
                     fileName: str = None,
                     text: str = None,
                     selectionStartLine: str = None,
                     selectionStartColumn: str = None,
                     selectionEndLine: str = None,
                     selectionEndColumn: str = None,
                     **_) -> 'Session':
        """Create new session instance and save to redis."""
        session = Session(id=uuid4().hex,
                          fileName=fileName,
                          text=text,
                          selectionStartLine=selectionStartLine,
                          selectionStartColumn=selectionStartColumn,
                          selectionEndLine=selectionEndLine,
                          selectionEndColumn=selectionEndColumn)
        await session.save()
        return session

    async def get(self, id: str) -> 'Session':
        """Get session by id."""
        serialized = await db.redis.get(_get_key(id))
        if not serialized:
            return

        data = json.loads(serialized)
        return Session(**data)


class Session(_SessionEntity):
    objects = SessionManager()

    async def save(self):
        """Save session to redis."""
        serialized = json.dumps(self._asdict())
        entry_key = _get_key(self.id)
        await db.redis.set(entry_key, serialized)
        await db.redis.publish(_get_channel_key(self.id),
                               serialized)

    async def update(self, **kwargs) -> 'Session':
        """Update session in redis."""
        session = self._replace(**kwargs)
        await session.save()
        return session

    def subscribe(self) -> 'Subscription':
        """Subscribe to session updates."""
        return Subscription(self)

    @property
    def as_dict(self):
        return self._asdict()


class Subscription(db.Subscription):
    """Subscription to PUB/SUB with session updates."""

    def __init__(self, session: Session):
        key = _get_channel_key(session.id)
        super().__init__([key])

    def _map(self, content: str) -> Session:
        data = json.loads(content)
        return Session(**data)
