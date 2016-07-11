import json

import pytest

from code_view import db


def test_key():
    assert db.key('test') == 'session:test'


@pytest.mark.asyncio
async def test_save():
    session = db.Session('test',
                         'test.py',
                         'print 123',
                         10, 11, 12, 13)
    await db.save(session)
    data = await db.redis.get(db.key('test'))
    assert json.loads(data) == session._asdict()


@pytest.mark.asyncio
async def test_create():
    session_1 = await db.create()
    session_2 = await db.create()
    assert session_1.id != session_2.id
    assert await db.redis.get(db.key(session_1.id)) is not None
    assert await db.redis.get(db.key(session_2.id)) is not None


class TestGet:
    @pytest.mark.asyncio
    async def test_exists(self):
        session = await db.create()
        assert await db.get(session.id) == session

    @pytest.mark.asyncio
    async def test_not_exists(self):
        assert await db.get('123456789') is None
