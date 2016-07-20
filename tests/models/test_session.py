import pytest
from code_view.models.session import Session


async def test_save():
    session = Session('test',
                      'test.py',
                      'print 123',
                      10, 11, 12, 13)
    await session.save()
    db_session = await Session.objects.get(session.id)
    assert db_session == session


async def test_create():
    session_1 = await Session.objects.create()
    session_2 = await Session.objects.create()
    assert session_1.id != session_2.id
    assert await Session.objects.get(session_1.id) == session_1
    assert await Session.objects.get(session_2.id) == session_2


class TestGet:
    async def test_exists(self):
        session = await Session.objects.create()
        assert await Session.objects.get(session.id) == session

    async def test_not_exists(self):
        assert await Session.objects.get('123456789') is None


async def test_update():
    session = await Session.objects.create()
    session = await session.update(fileName='test.py')
    received = await Session.objects.get(session.id)
    assert session == received


async def test_subscription():
    session = await Session.objects.create()
    subscription = session.subscribe()
    iterator = await subscription.__aiter__()
    session = await session.update(fileName='main.py')
    received = await iterator.__anext__()
    assert session == received
    session = await session.update(fileName='main.py', text='print 123')
    received = await iterator.__anext__()
    assert session == received


async def test_as_dict():
    session = await Session.objects.create()
    assert session.as_dict == session._asdict()
