from asyncio import set_event_loop, sleep

import pytest
from threading import Thread
from aiohttp import WSServerHandshakeError

from code_view.models.session import Session


class TestSubscribeToSession:
    async def test_not_found(self, client):
        with pytest.raises(WSServerHandshakeError) as e:
            await client.ws_connect('/channel/session/test/')

        assert e.value.code == 404

    async def test_receive_updates(self, loop, client):
        session = await Session.objects.create()

        conn = await client.ws_connect('/channel/session/{}/'.format(
            session.id))

        # Wait for subscription:
        await sleep(0.5)

        session = await session.update(fileName='test.py')
        msg = await conn.receive()

        assert msg.json() == session.as_safe_dict
