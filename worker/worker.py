import asyncio

from . import config
from .connection import Connection


class Worker:
    def __init__(self):
        self.conn = Connection(config.config.server_uri)

    async def _run(self):
        t = asyncio.create_task(self.conn.handler())
        i = 0
        try:
            while True:
                await asyncio.sleep(10)
                await self.conn.update_status({
                    "iteration": i,
                    "task": "Idle"
                })
                print("Worker Loop")
                print(f"Average ping: {self.conn.avg_ping:.2f} ms")
        except KeyboardInterrupt:
            await self.conn.close()

    def start(self):
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            pass
