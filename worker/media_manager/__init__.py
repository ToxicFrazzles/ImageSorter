import asyncio
import hashlib
import json
from asyncio import Task

import aiofiles
import aiohttp

from .. import config
from .connection import Connection


class MediaManager:
    _logging_ping = False
    _ping_logger: Task
    session: aiohttp.ClientSession

    def __init__(self):
        self.ws = Connection(config.config.websocket_uri)

    async def start(self):
        # Get an aiohttp session
        cookie_jar = aiohttp.CookieJar(unsafe=True)
        self.session = aiohttp.ClientSession(base_url=config.config.api_uri, cookie_jar=cookie_jar)

        # Connect the websocket
        asyncio.create_task(self.ws.handler())

        # Authenticate via HTTP too
        async with self.session.get("/auto_tag/auth/") as r:
            data = json.loads(await r.content.read())
        m = hashlib.sha256()
        m.update(config.config.client_secret.encode())
        m.update(data["challenge"].encode())
        answer = m.hexdigest()
        async with self.session.post("/auto_tag/auth/",
                                json={"client_id": config.config.client_id, "response": answer}) as r:
            print(await r.content.read())

    async def download_media_file(self, file_id: int):
        async with self.session.get(f"/auto_tag/media/{file_id}/") as r:
            r.raise_for_status()
            filename = r.headers["Content-Disposition"].split(";")[1].split("=")[1].strip("\"")
            async with aiofiles.open(config.config.temp_directory / filename, "wb") as f:
                async for data in r.content.iter_chunked(8192):
                    await f.write(data)
        return (config.config.temp_directory / filename).resolve()

    async def update_status(self, status):
        await self.ws.update_status(status)

    async def _ping_log_worker(self):
        while self._logging_ping:
            await asyncio.sleep(5)
            print(f"Average ping: {self.ws.avg_ping:.2f} ms")

    async def log_ping(self, stop=False):
        if self._logging_ping and stop:
            self._ping_logger.cancel()
            self._logging_ping = False
        elif not self._logging_ping and not stop:
            self._logging_ping = True
            asyncio.create_task(self._ping_log_worker())

