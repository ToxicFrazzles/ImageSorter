import asyncio
import hashlib
import json

import aiohttp

from . import config
from .media_manager import MediaManager


class Worker:
    def __init__(self):
        self.manager = MediaManager()

    async def _run(self):
        await self.manager.start()
        await self.manager.log_ping()
        i = 0
        while True:
            await asyncio.sleep(10)
            await self.manager.update_status({
                "iteration": i,
                "task": "Idle"
            })
            print("Worker Loop")

    def start(self):
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            pass
