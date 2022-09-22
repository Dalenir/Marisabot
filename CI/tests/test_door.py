import asyncio

import pytest

from Marisa import main
from handlers import main_hand

pytestmark = pytest.mark.anyio


@pytest.fixture(scope='module')
def anyio_backend():
    return 'asyncio'


class TestDoor:

    async def test_bot_door(self):
        try:
            await asyncio.wait_for(main(), 5)
        except asyncio.exceptions.TimeoutError:
            await main_hand.router.emit_shutdown()
