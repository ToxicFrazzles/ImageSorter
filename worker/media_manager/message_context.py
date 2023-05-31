from typing import Dict
from common import message_codes as mc


class MessageContext:
    def __init__(self, manager, msg_obj: Dict):
        self._manager = manager
        self.op_code = msg_obj.get('opcode', mc.UNKNOWN)
        self.msg = msg_obj

    async def reply(self, response: Dict):
        await self._manager.send_ws(response)
