import json
from code_view.models.session import Session


async def test_create_session(client):
    response = await client.post('/api/session/')
    assert response.status == 201
    data = await response.json()
    assert set(data) == {'id', 'secureToken', 'fileName', 'text',
                         'selectionStartLine', 'selectionStartColumn',
                         'selectionEndLine', 'selectionEndColumn'}
    assert data['id'] is not None


class TestUpdateSession:
    async def test_wrong(self, client):
        inst = await Session.objects.create()
        response = await client.put('/api/session/test/',
                                    data=json.dumps({'id': inst.id}))
        assert response.status == 400
        assert await Session.objects.get(inst.id) == inst

    async def test_not_found(self, client):
        response = await client.put('/api/session/test/',
                                    data=json.dumps({'id': 'test'}))
        assert response.status == 404

    async def test_wrong_token(self, client):
        inst = await Session.objects.create()
        response = await client.put('/api/session/{}/'.format(inst.id),
                                    data=json.dumps({'id': inst.id,
                                                     'secureToken': 'test'}))
        assert response.status == 403

    async def test_correct(self, client):
        inst = await Session.objects.create()
        response = await client.put(
            '/api/session/{}/'.format(inst.id), data=json.dumps({
                'id': inst.id,
                'secureToken': inst.secureToken,
                'fileName': 'main.py',
                'text': 'print 123',
                'selectionStartLine': 10,
                'selectionStartColumn': 11,
                'selectionEndLine': 12,
                'selectionEndColumn': 13}))

        assert response.status == 200

        data = await response.json()
        inst = await Session.objects.get(inst.id)

        assert inst.as_dict == data == {
            'id': inst.id,
            'secureToken': inst.secureToken,
            'fileName': 'main.py',
            'text': 'print 123',
            'selectionStartLine': 10,
            'selectionStartColumn': 11,
            'selectionEndLine': 12,
            'selectionEndColumn': 13}


class TestGetSession:
    async def test_not_found(self, client):
        response = await client.get('/api/session/test/')
        assert response.status == 404

    async def test_found(self, client):
        inst = await Session.objects.create()
        response = await client.get('/api/session/{}/'.format(inst.id))
        assert response.status == 200
        data = await response.json()
        assert data == inst.as_safe_dict
