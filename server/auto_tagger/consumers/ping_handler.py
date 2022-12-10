import json
from common import message_codes as mc
from .base_consumer import BaseConsumer


class PingHandler(BaseConsumer):
    async def _ping_handler(self, msg_obj: dict):
        await self.send(json.dumps({
            "opcode": mc.PONG,
            "time": msg_obj["time"]
        }))

    handlers = {
        mc.PING: _ping_handler
    }
