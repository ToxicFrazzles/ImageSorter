import asyncio
import hashlib
import json
import socket
import time

import websockets
import websockets.exceptions
from websockets.client import connect

from common import message_codes as mc
from worker import config


class Connection:
    def __init__(self, server):
        self.server = server
        self.conn = None
        self.reconnect = True
        self.current_status = {}
        self.avg_ping = 0

    async def close(self):
        self.reconnect = False
        await self.conn.close()

    async def _consumer_handler(self):
        try:
            async for message in self.conn:
                await self._consumer(json.loads(message))
        except websockets.ConnectionClosedError:
            print("Connection closed")

    async def _producer_handler(self):
        while True:
            message = await self._producer()
            await self.send(message)

    async def handler(self):
        while self.reconnect:
            try:
                async with connect(self.server) as self.conn:
                    consumer_task = asyncio.create_task(self._consumer_handler())
                    producer_task = asyncio.create_task(self._producer_handler())
                    done, pending = await asyncio.wait(
                        [consumer_task, producer_task],
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    for task in pending:
                        task.cancel()
            except socket.gaierror:
                print("Socket error")
                await asyncio.sleep(5)
            except websockets.ConnectionClosedError:
                print("Connection closed")
                await asyncio.sleep(10)
            except ConnectionRefusedError:
                print("Connection refused... Please check the URL and connection")
                await asyncio.sleep(30)

    async def _consumer(self, msg_obj: dict):
        op_code = msg_obj.get("opcode", -1)
        if op_code == mc.PONG:
            await self._pong_consumer(msg_obj)
        elif op_code == mc.HELLO:
            await self._hello_consumer(msg_obj)
        elif op_code == mc.AUTHED:
            print("Authenticated")
            await self._send_status()
        else:
            print(msg_obj)

    async def _producer(self):
        await asyncio.sleep(1)
        return {"opcode": mc.PING, "time": time.time()}

    async def _pong_consumer(self, msg_obj: dict):
        dur = (time.time()-msg_obj["time"])*1000
        self.avg_ping = (dur + self.avg_ping)/2

    async def _hello_consumer(self, msg_obj: dict):
        m = hashlib.sha256()
        m.update(config.config.client_secret.encode())
        m.update(msg_obj["challenge"].encode())
        answer = m.hexdigest()
        await self.send({
            "opcode": mc.AUTH,
            "client_id": config.config.client_id,
            "response": answer
        })

    async def send(self, message_obj: dict):
        await self.conn.send(json.dumps(message_obj))

    async def _send_status(self):
        out = self.current_status.copy()
        out.update({
            "opcode": mc.STATUS,
            "does_inference": config.config.do_inference,
            "does_training": config.config.do_training
        })
        try:
            await self.send(out)
        except websockets.ConnectionClosedError:
            pass

    async def update_status(self, status_obj: dict):
        self.current_status = status_obj
        await self._send_status()
