import json
from unittest.mock import Mock

import pytest
from code_view import handlers
from code_view import db


async def stream(content):
    return content


@pytest.mark.asyncio
async def test_create_session():
    response = await handlers.create_session(Mock())
    assert response.status == 201
    data = json.loads(response.body.decode())
    assert data.keys() == {'id', 'fileName', 'text',
                           'selectionStartLine', 'selectionStartColumn',
                           'selectionEndLine', 'selectionEndColumn'}
    assert data['id'] is not None


class TestUpdateSession:
    @pytest.mark.asyncio
    async def test_wrong(self):
        session = await db.create()
        request = Mock(match_info={'id': 'test'})
        request.json.return_value = stream({'id': session.id})
        response = await handlers.update_session(request)
        assert response.status == 400
        assert await db.get(session.id) == session

    @pytest.mark.asyncio
    async def test_correct(self):
        session = await db.create()
        request = Mock(match_info={'id': session.id})
        request.json.return_value = stream({
            'id': session.id,
            'fileName': 'main.py',
            'text': 'print 123',
            'selectionStartLine': 10,
            'selectionStartColumn': 11,
            'selectionEndLine': 12,
            'selectionEndColumn': 13})
        response = await handlers.update_session(request)
        assert response.status == 200
        data = json.loads(response.body.decode())
        session = await db.get(session.id)
        assert session._asdict() == data == db.Session(
            session.id, 'main.py', 'print 123', 10, 11, 12, 13)._asdict()


class TestGetSession:
    @pytest.mark.asyncio
    async def test_not_found(self):
        request = Mock(match_info={'id': '123456789'})
        response = await handlers.get_session(request)
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_found(self):
        session = db.Session(
            'id', 'main.py', 'print 123', 10, 11, 12, 13)
        await db.save(session)
        request = Mock(match_info={'id': session.id})
        response = await handlers.get_session(request)
        data = json.loads(response.body.decode())
        assert data == session._asdict()
