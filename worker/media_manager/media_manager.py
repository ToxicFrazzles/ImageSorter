import asyncio
import hashlib
import json
import socket
import time
from typing import Dict, List

import aiohttp
import websockets
from websockets.client import connect

from .message_context import MessageContext
from .. import config
from .module import Module
from common import message_codes as mc


class MediaManager:
    _ws: websockets.WebSocketClientProtocol
    _modules: List[Module] = []

    def __init__(self):
        self.current_status = {}
        self._running = False

    async def _run(self):
        cookie_jar = aiohttp.CookieJar(unsafe=True)
        self._sess: aiohttp.ClientSession = aiohttp.ClientSession(config.config.api_uri, cookie_jar=cookie_jar)
        asyncio.create_task(self._authenticate_http())
        self._ws_connected = asyncio.Event()
        async for self._ws in connect(config.config.websocket_uri):
            try:
                self._ws_connected.set()
                await self._send_status()
                consumer_task = asyncio.create_task(self._consumer_handler())
                producer_task = asyncio.create_task(self._producer_handler())
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for task in pending:
                    task.cancel()
            except socket.gaierror:
                self._ws_connected.clear()
                print("Socket Error")
            except websockets.ConnectionClosedError:
                self._ws_connected.clear()
                print("Connection closed")
            except ConnectionRefusedError:
                self._ws_connected.clear()
                print("Connection refused...")
                await asyncio.sleep(10)
            except KeyboardInterrupt:
                self._ws_connected.clear()
                raise
            except Exception as e:
                self._ws_connected.clear()
                print(e)

    def run(self):
        self._running = True
        asyncio.run(self._run())

    async def _authenticate_http(self):
        async with self._sess.get("/auto_tag/auth/") as r:
            data = json.loads(await r.content.read())
        m = hashlib.sha256()
        m.update(config.config.client_secret.encode())
        m.update(data["challenge"].encode())
        answer = m.hexdigest()
        async with self._sess.post(
                "/auto_tag/auth/",
                json={"client_id": config.config.client_id, "response": answer}) as r:
            result = json.loads(await r.content.read())
            if "Success" in result:
                print("HTTP Authenticated")
            else:
                print("HTTP Failed Authentication!")

    async def send_ws(self, msg_obj: Dict):
        await self._ws.send(json.dumps(msg_obj))

    async def _consumer_handler(self):
        try:
            async for message in self._ws:
                ctx = MessageContext(self, json.loads(message))
                handled = False
                for module in self._modules:
                    handled |= await module.dispatch(ctx)
                if not handled:
                    print(ctx.msg)
        except websockets.ConnectionClosedError:
            print("Connection closed")

    async def _producer_handler(self):
        while True:
            message = await self._producer()
            await self.send_ws(message)

    async def _producer(self):
        await asyncio.sleep(1)
        return {"opcode": mc.PING, "time": time.time()}

    def register_module(self, module_instance: Module):
        self._modules.append(module_instance)

    async def _send_status(self):
        out = self.current_status.copy()
        out.update({
            "opcode": mc.STATUS,
            "does_inference": config.config.do_inference,
            "does_training": config.config.do_training
        })
        try:
            await self.send_ws(out)
        except websockets.ConnectionClosedError:
            pass

    async def update_status(self, status_obj: dict):
        self.current_status = status_obj
        await self._send_status()

    async def get_new_task(self):
        await self.send_ws({
            "opcode": mc.GET_TASK,
            "inference": config.config.do_inference,
            "training": config.config.do_training
        })
